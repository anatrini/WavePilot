import argparse
import asyncio
import time
from threading import Thread

#import torch
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from pythonosc import udp_client
#from torch import nn

from constants import IP_ADDRESS, IN_PORT, OUT_PORT
from data import DataLoader
from interpolator import RBFInterpolation
from logger import setup_logger
from model import VectorReducer
from serialization import load_model, save_model
from utils import get_activation_function, get_hyperparams_from_log
from visualizer import Visualize



log = setup_logger("Main VAE")


def get_arguments():
    parser = argparse.ArgumentParser(description="Train a Variational Autoencoder (VAE) for preset reduction.")

    # Dataset (Obbligatorio)
    parser.add_argument("-f", "--filepath", dest="filepath", type=str, help="Dataset of presets to be reduced.")

    # Modello pre-addestrato (Opzionale)
    parser.add_argument("-p", "--pretrained-model", dest="pretrained_model", type=str, default=None, help="Pretrained model file.")

    # Sessione di ottimizzazione
    parser.add_argument("-o", "--optimizer-session", dest="optimizer_session", type=str, default=None, help="Log file of a previous optimization session.")

    parser.add_argument("-s", "--save-model-path", dest="save_model_path", help="If set save model to this path after training.")

    return parser.parse_args()


def run_flask(app, socketio, reduced_data):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/data")
    def get_data():
        return jsonify(reduced_data.tolist())

    socketio.run(app)


async def main():
    args = get_arguments()
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, OUT_PORT)

    start_time = time.time()

    filepath = args.filepath
    pretrained_model = args.pretrained_model
    optimizer_session = args.optimizer_session
    save_model_path = args.save_model_path

    # if args.optimizer_session:
    #     params = get_hyperparams_from_log(args.optimizer_session)
    #     n_layers = params["vae"]["n_layers"]
    #     activation = get_activation_function(params["vae"]["activation_function"])
    #     n_epochs = params["vae"]["num_epochs"]
    #     learning_rate = params["vae"]["learning_rate"]
    #     weight_decay = params["vae"]["weight_decay"]
    #     layer_dim = params["vae"]["layer_dim"]
    #     kl_beta = params["vae"]["kl_beta"]
    #     mse_beta = params["vae"]["mse_beta"]
    #     smoothing = params["rbf"]["smoothing"]
    #     kernel = params["rbf"]["kernel"]
    #     epsilon = params["rbf"]["epsilon"]
    #     degree = params["rbf"]["degree"]
    # else:
    #     n_layers = args.n_layers
    #     activation = args.activation_function
    #     n_epochs = args.n_epochs
    #     learning_rate = args.learning_rate
    #     weight_decay = args.weight_decay
    #     layer_dim = args.layer_dim
    #     kl_beta = args.kl_beta
    #     mse_beta = args.mse_beta
    #     smoothing = args.smoothing
    #     kernel = args.kernel
    #     epsilon = args.epsilon
    #     degree = args.degree

    # try:
    #     loader = DataLoader(filepath)
    #     original_data = loader.load_presets()

    #     if pretrained_model is not None:
    #         pmodel = load_model(pretrained_model)
    #         reducer = VectorReducer(pretrained_model)
    #     else:
    #         reducer = VectorReducer(
    #             original_data, learning_rate, weight_decay, n_layers, layer_dim, activation, kl_beta, mse_beta
    #         )

    #     reducer.train_vae(n_epochs)
    #     reduced_data, reconstructed_data = reducer.vae()

    # except FileNotFoundError:
    #     logging.error("You must provide at least a dataset!")
    #     exit(1)

    # interpolator = RBFInterpolation(reduced_data, reconstructed_data, smoothing, kernel, epsilon, degree)
    # visualizer = Visualize(reduced_data, app, socketio)

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # logging.info(f"Computation time: {elapsed_time} sec.")

    # # Start Flask in a separate thread
    # flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
    # flask_thread.start()

    # # Run asyncio event loop
    # await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)
    try:
        # CASE 1: Load pretrained model directly
        if pretrained_model and not optimizer_session:
            pmodel, _ = load_model(pretrained_model)
            reducer = VectorReducer(pretrained_model=pmodel)
            reduced_data, reconstructed_data = reducer.vae()

        # CASE 2: Load optimizer session and train
        elif optimizer_session and not pretrained_model:
            loader = DataLoader(filepath)
            original_data = loader.load_presets()
            params = get_hyperparams_from_log(optimizer_session)

            reducer = VectorReducer(
                df=original_data,
                learning_rate=params["vae"]["learning_rate"],
                weight_decay=params["vae"]["weight_decay"],
                n_layers=params["vae"]["n_layers"],
                layer_dim=params["vae"]["layer_dim"],
                activation=get_activation_function(params["vae"]["activation_function"]),
                kl_beta=params["vae"]["kl_beta"],
                mse_beta=params["vae"]["mse_beta"],
            )

            reducer.train_vae(params["vae"]["num_epochs"])
            reduced_data, reconstructed_data = reducer.vae()

            if save_model_path:
                save_model(
                    model=reducer.model,
                    input_dim=original_data.shape[1],
                    n_layers=params["vae"]["n_layers"],
                    layer_dim=params["vae"]["layer_dim"],
                    activation_name=params["vae"]["activation_function"],
                    filepath=save_model_path
                )

        else:
            log.error("You must specify either --pretrained-model or --optimizer-session (but not both).")
            return

        interpolator = RBFInterpolation(
            reduced_data,
            reconstructed_data,
            params["rbf"]["smoothing"],
            params["rbf"]["kernel"],
            params["rbf"]["epsilon"],
            params["rbf"]["degree"]
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
        log.error("Unhandled error: %s", e)
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
