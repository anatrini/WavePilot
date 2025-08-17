import time
from threading import Thread

import numpy as np
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from pythonosc import udp_client
from scipy.spatial.distance import pdist

from constants import IP_ADDRESS, SEND_PORT, RECEIVE_PORT, RBF_FIXED_EPSILON_KERNELS
from data import DataLoader
from interpolator import RBFInterpolation
from logger import setup_logger
from model import VectorReducer, TrainConfig
from serialization import load_model, save_model
from utils import get_hyperparams_from_log, LatentScaler
from visualizer import Visualize


log = setup_logger("VAE and Interpolator")


def run_flask(app, socketio, reduced_data):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/data")
    def get_data():
        return jsonify(reduced_data.tolist())

    socketio.run(app)


async def main(filepath, pretrained_model_path, optimizer_session, save_model_path):

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, RECEIVE_PORT)

    start_time = time.time()

    # Basic CLI validation
    if not filepath:
        log.error("You must provide a dataset file with --filepath.")
        return
    if not (pretrained_model_path or optimizer_session):
        log.error("You must specify either --pretrained-model or --optimizer-session.")
        return
    if pretrained_model_path and optimizer_session:
        log.error("You must specify only one between --pretrained-model or --optimizer-session.")
        return

    loader = DataLoader(filepath)
    original_data = loader.load_presets()

    try:
        # --- Build / load VAE ---
        rbf_params = None

        if pretrained_model_path:
            # Case 1: load pretrained checkpoint
            model, vae_params, rbf_package = load_model(pretrained_model_path)
            rbf_params = rbf_package.get("params", {})

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
                epochs=vae_params["max_epochs"],
                lr=vae_params["learning_rate"],
                kl_beta=vae_params.get("kl_beta", 0.0),
                deterministic=True,
                hidden_dims=None,
                grad_clip=vae_params.get("grad_clip", 1.0),
                batch_size=vae_params.get("batch_size", 0),
            )
            # Hidden-dims policy knobs
            setattr(cfg, "width_scale", vae_params["width_scale"])
            setattr(cfg, "depth",       vae_params["depth"])
            setattr(cfg, "round_to",    vae_params["round_to"])

            reducer.fit(cfg)

        # --- Deterministic latent (μ) ---
        reduced_data = reducer.transform()

        # --- External latent normalisation (z-score) ---
        NORMALISE_LATENT = True
        if NORMALISE_LATENT:
            scaler = LatentScaler().fit(reduced_data)
            Z_std = scaler.transform(reduced_data)
        else:
            scaler = None
            Z_std = reduced_data

        # --- Geometry for epsilon: median pairwise distance in the fitting space ---
        if Z_std.shape[0] >= 2:
            dvec = pdist(Z_std, metric="euclidean")
            median_dist = float(np.median(dvec)) if dvec.size > 0 else 1.0
        else:
            median_dist = 1.0

        # --- Compute epsilon (fixed for some kernels; relative otherwise) ---
        kernel = rbf_params["kernel"]
        epsilon = rbf_params.get("epsilon")
        if epsilon is None:
            epsilon_scale = rbf_params["epsilon_scale"]
            epsilon = 1.0 if kernel in RBF_FIXED_EPSILON_KERNELS else max(1e-12, float(epsilon_scale) * median_dist)

        # --- Instantiate interpolator on the SAME latent space used for the visualiser ---
        interpolator = RBFInterpolation(
            Z_std,                         # latent fitting space (z-scored if NORMALISE_LATENT=True)
            original_data,                 # targets in [0,1]
            rbf_params["smoothing"],
            kernel,
            epsilon,
            degree=rbf_params["degree"]
        )

        # The visualiser must see the same latent space used to fit the RBF
        visualizer = Visualize(Z_std, app, socketio)

        elapsed_time = time.time() - start_time
        log.info("Training and setup completed in %.2f seconds.", elapsed_time)

        flask_thread = Thread(target=run_flask, args=(app, socketio, Z_std))
        flask_thread.start()

        # Optional: save consolidated checkpoint when training from optimiser session
        if (not pretrained_model_path) and save_model_path:
            save_model(
                reducer=reducer,
                vae_params=vae_params,
                rbf_params=rbf_params,
                filepath=save_model_path,
                latent_scaler=scaler,
                rbf_interpolator=None,   # your RBFInterpolation wraps SciPy internally
                Z_std=Z_std,
                original_data=original_data,
                median_dist=median_dist
            )

        await visualizer.run(IP_ADDRESS, SEND_PORT, interpolator, osc_client)

    except FileNotFoundError as e:
        log.error("File not found: %s", e)
        exit(1)
    except Exception as e:
        log.error("Unhandled error: %s", e, exc_info=True)
        exit(1)
