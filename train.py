import time
from threading import Thread

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from pythonosc import udp_client

from constants import IP_ADDRESS, IN_PORT, OUT_PORT
from data import DataLoader
from interpolator import RBFInterpolation
from logger import setup_logger
from model import VectorReducer
from serialization import load_model, save_model
from utils import get_activation_function, get_hyperparams_from_log
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
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, OUT_PORT)

    start_time = time.time()

    # Check valid combinations
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
        reduced_data = None
        reconstructed_data = None

        if pretrained_model_path:
            # CASE 1: Load pretrained model (.pt), extract params from checkpoint
            model, vae_params, rbf_params = load_model(pretrained_model_path)
            reducer = VectorReducer(df=original_data, pretrained_model=model)
            reduced_data, reconstructed_data = reducer.vae()

        elif optimizer_session:
            # CASE 2: Train from optimizer log
            full_params = get_hyperparams_from_log(optimizer_session)
            vae_params = full_params["vae"]
            rbf_params = full_params["rbf"]

            reducer = VectorReducer(
                df=original_data,
                learning_rate=vae_params["learning_rate"],
                weight_decay=vae_params["weight_decay"],
                n_layers=vae_params["n_layers"],
                layer_dim=vae_params["layer_dim"],
                activation=get_activation_function(vae_params["activation_function"]),
                kl_beta=vae_params["kl_beta"],
                mse_beta=vae_params["mse_beta"],
            )

            reducer.train_vae(vae_params["num_epochs"])
            reduced_data, reconstructed_data = reducer.vae()

            # Save model if requested
            if save_model_path:
                save_model(
                    model=reducer.model,
                    vae_params={
                        "input_dim": original_data.shape[1],
                        "n_layers": vae_params["n_layers"],
                        "layer_dim": vae_params["layer_dim"],
                        "activation_function": vae_params["activation_function"]
                    },
                    rbf_params=rbf_params,
                    filepath=save_model_path
                )

        # Initialize interpolator with RBF params
        interpolator = RBFInterpolation(
            reduced_data,
            reconstructed_data,
            rbf_params["smoothing"],
            rbf_params["kernel"],
            rbf_params["epsilon"],
            rbf_params["degree"]
        )

        visualizer = Visualize(reduced_data, app, socketio)

        elapsed_time = time.time() - start_time
        log.info("Training and setup completed in %.2f seconds.", elapsed_time)

        flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
        flask_thread.start()

        await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)

    except FileNotFoundError as e:
        log.error("File not found: %s", e)
        exit(1)
    except Exception as e:
        log.error("Unhandled error: %s", e, exc_info=True)
        exit(1)