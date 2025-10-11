# train.py
# Flask + Socket.IO bootstrap with asynchronous main.
# British English comments. No nested functions or classes.

import time
from threading import Thread

import numpy as np
from flask import Flask
from flask_socketio import SocketIO
from pythonosc import udp_client
from scipy.spatial.distance import pdist

from constants import (
    IP_ADDRESS, SEND_PORT, FORWARD_PORT, WEBAPP_HOST, WEBAPP_PORT,
    RBF_FIXED_EPSILON_KERNELS,
    FINAL_EPOCHS,
    NORMALISE_LATENT_DEFAULT,
    GRAD_CLIP_DEFAULT,
    DEFAULT_BATCH_SIZE,
    DEFAULT_KL_BETA,
    GLOBAL_SEED
)
from data import DataLoader
from interpolator import RBFInterpolation
from logger import setup_logger
from model import VectorReducer, TrainConfig
from serialization import load_model, save_model
from socket_handlers import cursor_move, register_addr_list
from utils import get_hyperparams_from_log, LatentScaler, set_global_seeds, load_osc_addresses
from visualizer import Visualize
from web_routes import index_route, data_route
import os


log = setup_logger("DVAE and Interpolator")


def run_flask(app, socketio, latent_data):
    """
    Run the Flask + Socket.IO development server in its own thread.
    The latent data is exposed via app.config for the HTTP routes.
    """
    # Make latent data available to route handlers via current_app.config
    app.config["LATENT_DATA"] = latent_data

    # Register routes defined in web_routes.py
    app.add_url_rule("/",     endpoint="index", view_func=index_route, methods=["GET"])
    app.add_url_rule("/data", endpoint="data",  view_func=data_route,  methods=["GET"])

    # Start web server + Socket.IO (default bind; adjust externally if needed)
    socketio.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT, allow_unsafe_werkzeug=True)


async def main(filepath, pretrained_model_path, optimizer_session, save_model_path):
    """
    Asynchronous entry point:
      - trains or loads the VAE, builds the RBF interpolator,
      - starts Flask/Socket.IO in a background thread,
      - starts the OSC ingress (visualiser) and awaits it.
    """

    # Set global seed for reproducibility
    set_global_seeds(GLOBAL_SEED)

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)

    # Disable caching for all responses to force browser to reload JS files
    @app.after_request
    def add_no_cache_headers(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # IMPORTANT: Web → ReaLearn egress must target SEND_PORT.
    # The controller/device never listens here; ReaLearn does.
    osc_client = udp_client.SimpleUDPClient("127.0.0.1", SEND_PORT)

    start_time = time.time()

    # Basic CLI validation
    if not filepath:
        log.error("You must provide a dataset file with --filepath!")
        return
    if not (pretrained_model_path or optimizer_session):
        log.error("You must specify either --pretrained-model or --optimizer-session!")
        return
    if pretrained_model_path and optimizer_session:
        log.error("You must specify only one between --pretrained-model or --optimizer-session!")
        return

    loader = DataLoader(filepath)
    original_data = loader.load_presets()

    try:
        # --- Build / load VAE ---
        rbf_params = None
        latent_scaler_ckpt = None

        if pretrained_model_path:
            # Case 1: load pretrained checkpoint
            model, vae_params, rbf_package = load_model(pretrained_model_path)
            rbf_params = rbf_package.get("params", {})
            latent_scaler_ckpt = rbf_package.get("latent_scaler", None)

            reducer = VectorReducer(original_data, latent_dim=vae_params["latent_dim"])
            reducer.model = model.to(reducer.device)
            reducer.model.eval()

        else:
            # Case 2: train from optimiser log
            full_params = get_hyperparams_from_log(optimizer_session)
            vae_params = full_params["vae"]
            rbf_params = full_params["rbf"]

            reducer = VectorReducer(original_data, latent_dim=vae_params["latent_dim"])

            cfg = TrainConfig(
                epochs=FINAL_EPOCHS,
                lr=vae_params["learning_rate"],
                kl_beta=vae_params.get("kl_beta", DEFAULT_KL_BETA),
                deterministic=True,
                hidden_dims=None,
                grad_clip=vae_params.get("grad_clip", GRAD_CLIP_DEFAULT),
                batch_size=vae_params.get("batch_size", DEFAULT_BATCH_SIZE),
            )
            # Hidden-dims policy knobs
            setattr(cfg, "width_scale", vae_params["width_scale"])
            setattr(cfg, "depth",       vae_params["depth"])
            setattr(cfg, "round_to",    vae_params["round_to"])

            reducer.fit(cfg, show_progress=True)

        # --- Extract deterministic latent (μ) ---
        reduced_data = reducer.transform()

        # --- Apply external latent normalisation (z-score) ---
        Z_std = reduced_data
        scaler = None
        if pretrained_model_path and (latent_scaler_ckpt is not None):
            scaler = latent_scaler_ckpt
            Z_std = scaler.transform(reduced_data)
        elif NORMALISE_LATENT_DEFAULT:
            scaler = LatentScaler().fit(reduced_data)
            Z_std = scaler.transform(reduced_data)

        assert np.all(np.isfinite(Z_std)), "Non-finite values detected in Z_std."

        # --- Compute geometry for epsilon: median pairwise distance in fitting space ---
        if Z_std.shape[0] >= 2:
            dvec = pdist(Z_std, metric="euclidean")
            median_dist = float(np.median(dvec)) if dvec.size > 0 else 1.0
        else:
            median_dist = 1.0

        # --- Apply kernel/epsilon policy ---
        kernel = rbf_params["kernel"]
        if kernel in RBF_FIXED_EPSILON_KERNELS:
            epsilon = None  # SciPy ignores epsilon for these kernels
        else:
            epsilon = float(rbf_params["epsilon_scale"]) * float(median_dist)

        # --- Instantiate interpolator on the same latent space used for the visualiser ---
        interpolator = RBFInterpolation(
            Z_std,                         # latent fitting space (z-scored if NORMALISE_LATENT=True)
            original_data,                 # targets in [0,1]
            rbf_params["smoothing"],
            kernel,
            epsilon,
            degree=rbf_params["degree"]
        )

        # Optional: save consolidated checkpoint when training from optimiser session
        if (not pretrained_model_path) and save_model_path:
            save_model(
                reducer=reducer,
                vae_params=vae_params,
                rbf_params=rbf_params,
                filepath=save_model_path,
                latent_scaler=scaler,
                rbf_interpolator=None,
                Z_std=Z_std,
                original_data=original_data,
                median_dist=median_dist
            )

        # --- Publish data to web and register routes ---
        app.config["LATENT_DATA"]  = Z_std
        app.config["PRESET_NAMES"] = loader.get_preset_names(Z_std.shape[0])

        app.add_url_rule("/",     "index_route", index_route, methods=["GET"])
        app.add_url_rule("/data", "data_route",  data_route,  methods=["GET"])

        # Expose dependencies to Socket.IO handlers
        app.config["INTERPOLATOR"] = interpolator
        app.config["OSC_CLIENT"]   = osc_client

        # Auto-detect and load OSC address list from addresses/*.json
        # Try to match the dataset filename to an addresses file
        dataset_basename = os.path.splitext(os.path.basename(filepath))[0]
        # Remove common suffixes like _test32, _random, etc to find the plugin name
        plugin_name = dataset_basename.split('_')[0].lower()

        addr_file = os.path.join("addresses", f"{plugin_name}.json")
        if os.path.exists(addr_file):
            addr_data = load_osc_addresses(addr_file)
            if isinstance(addr_data, list):
                app.config["OSC_ADDR_LIST"] = addr_data
                log.info("Loaded %d OSC addresses from %s", len(addr_data), addr_file)
            elif isinstance(addr_data, dict):
                app.config["OSC_ADDR_LIST"] = list(addr_data.values())
                log.info("Loaded %d OSC addresses from %s (dict)", len(addr_data), addr_file)
        else:
            log.warning("No OSC address file found at %s - addr_list must be provided by controller", addr_file)
            app.config["OSC_ADDR_LIST"] = []

        # Register the Socket.IO handler (browser → server)
        socketio.on_event("cursor_move", cursor_move)
        socketio.on_event("addr_list", register_addr_list)

        # The visualiser must see the same latent space used to fit the RBF
        visualizer = Visualize(Z_std, socketio)

        elapsed_time = time.time() - start_time
        log.info("Training and setup completed in %.2f seconds.", elapsed_time)

        # Start Flask in a separate thread (non-blocking for this async main)
        flask_thread = Thread(target=run_flask, args=(app, socketio, Z_std), daemon=True)
        flask_thread.start()

        # IMPORTANT: the OSC ingress for /cursor must bind on FORWARD_PORT (9901),
        # because the controller forwards the cursor to the web app on this port.
        await visualizer.run(IP_ADDRESS, FORWARD_PORT, interpolator, osc_client)

    except FileNotFoundError as e:
        log.error("File not found: %s", e)
        exit(1)
    except Exception as e:
        log.error("Unhandled error: %s", e, exc_info=True)
        exit(1)
