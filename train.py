import argparse
import asyncio
import time
from threading import Thread

import torch
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from pythonosc import udp_client
from torch import nn

from constants import IP_ADDRESS, IN_PORT, OUT_PORT
from data import DataLoader
from interpolator import RBFInterpolation
from logger import setup_logger
from model import VectorReducer
from utils import get_activation_function, get_hyperparams_from_log
from visualizer import Visualize



logging = setup_logger("Main VAE")


def get_arguments():
    parser = argparse.ArgumentParser(description="Train a Variational Autoencoder (VAE) for preset reduction.")

    # Dataset (Obbligatorio)
    parser.add_argument("-f", "--filepath", dest="filepath", type=str, required=True, help="Dataset of presets to be reduced.")

    # Modello pre-addestrato (Opzionale)
    parser.add_argument("-p", "--pretrained-model", dest="pretrained_model", type=str, default=None, help="Pretrained model file.")

    # Sessione di ottimizzazione
    parser.add_argument("-o", "--optimizer-session", dest="optimizer_session", type=str, default=None, help="Log file of a previous optimization session.")

    # Mascheramento dei parametri (Solo se ottimizzazione non è stata fatta)
    parser.add_argument("-m", "--mask-columns", dest="mask_columns", type=str, nargs="+", default=None, help="List of parameters to be masked (excluded).")

    # Iperparametri principali
    parser.add_argument("-n", "--num-layers", dest="n_layers", type=int, default=1, help="Number of hidden layers.")
    parser.add_argument("-l", "--layer-dim", dest="layer_dim", type=int, default=128, help="Size of hidden layers.")
    parser.add_argument("-a", "--activation", dest="activation_function", type=nn.Module, default=nn.ReLU(), help="Activation function.")

    # Training
    parser.add_argument("-e", "--epochs", dest="n_epochs", type=int, default=100, help="Number of training epochs.")
    parser.add_argument("-r", "--learning-rate", dest="learning_rate", type=float, default=1e-2, help="Learning rate.")
    parser.add_argument("-w", "--weight-decay", dest="weight_decay", type=float, default=1e-4, help="L1/L2 regularization.")

    # Parametri VAE
    parser.add_argument("-b", "--kl-beta", dest="kl_beta", type=float, default=0.05, help="KL divergence weight.")
    parser.add_argument("-s", "--mse-beta", dest="mse_beta", type=float, default=0.1, help="MSE loss weight.")

    # Parametri RBF Interpolation
    parser.add_argument("-k", "--kernel", dest="kernel", type=str, choices=["multiquadric", "inverse_multiquadric", "inverse_quadratic", "gaussian"], default="gaussian", help="Kernel type for RBF interpolation.")
    parser.add_argument("-x", "--epsilon", dest="epsilon", type=float, default=1.0, help="Epsilon value for RBF kernel.")
    parser.add_argument("-d", "--degree", dest="degree", type=int, default=None, help="Polynomial degree for RBF.")

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

    start_time = time.time()

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, OUT_PORT)

    args = get_arguments()
    filepath = args.filepath
    pretrained_model = args.pretrained_model

    if args.optimizer_session:
        params = get_hyperparams_from_log(args.optimizer_session)
        n_layers = params["vae"]["n_layers"]
        activation = get_activation_function(params["vae"]["activation_function"])
        n_epochs = params["vae"]["num_epochs"]
        learning_rate = params["vae"]["learning_rate"]
        weight_decay = params["vae"]["weight_decay"]
        layer_dim = params["vae"]["layer_dim"]
        kl_beta = params["vae"]["kl_beta"]
        mse_beta = params["vae"]["mse_beta"]
        smoothing = params["rbf"]["smoothing"]
        kernel = params["rbf"]["kernel"]
        epsilon = params["rbf"]["epsilon"]
        degree = params["rbf"]["degree"]
    else:
        n_layers = args.n_layers
        activation = args.activation_function
        n_epochs = args.n_epochs
        learning_rate = args.learning_rate
        weight_decay = args.weight_decay
        layer_dim = args.layer_dim
        kl_beta = args.kl_beta
        mse_beta = args.mse_beta
        smoothing = args.smoothing
        kernel = args.kernel
        epsilon = args.epsilon
        degree = args.degree

    try:
        loader = DataLoader(filepath)
        original_data = loader.load_presets()

        if pretrained_model is not None:
            pmodel = torch.load(pretrained_model)
            reducer = VectorReducer(
                original_data,
                learning_rate,
                weight_decay,
                n_layers,
                layer_dim,
                activation,
                kl_beta,
                mse_beta,
                pretrained_model=pmodel,
            )
        else:
            reducer = VectorReducer(
                original_data, learning_rate, weight_decay, n_layers, layer_dim, activation, kl_beta, mse_beta
            )

        reducer.train_vae(n_epochs)
        reduced_data, reconstructed_data = reducer.vae()

    except FileNotFoundError:
        logging.error("You must provide at least a dataset!")
        exit(1)

    interpolator = RBFInterpolation(reduced_data, reconstructed_data, smoothing, kernel, epsilon, degree)
    visualizer = Visualize(reduced_data, app, socketio)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Computation time: {elapsed_time} sec.")

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
    flask_thread.start()

    # Run asyncio event loop
    await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)


if __name__ == "__main__":
    asyncio.run(main())
