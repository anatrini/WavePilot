import argparse
import asyncio
import time

from model_vae import VectorReducer
from data import DataLoader
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from interpolator import RBFInterpolation
from logger import setup_logger
from pythonosc import udp_client
from torch import nn
from threading import Thread
from utils import *
from visualizer import Visualize


IP_ADDRESS = '127.0.0.1'
IN_PORT = 5105
OUT_PORT = 5106

logging = setup_logger('Main VAE')


def get_arguments():
    parser = argparse.ArgumentParser()

    # Small dataset of the presets to be reduced (Compulsory)
    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    # Large dataset of presets to pretrain the model (Optional)
    parser.add_argument('-F', '--filepath_pretrain',
                      dest='filepath_pretrain',
                      type=str,
                      default=None)
    
    parser.add_argument('-o', '--optimizer_session',
                      dest='optimizer_session',
                      type=str,
                      default=None,
                      help='Path to the log file of an optimization session.')
    
    parser.add_argument('-n', '--n_layers',
                      dest='n_layers',
                      type=int,
                      default=2,
                      help='Set the number of hidden layers used by the model.')
    
    parser.add_argument('-a', '--activation_function',
                      dest='activation_function',
                      type=nn.Module,
                      default=nn.ReLU(),
                      help='Set the activation function used by the model.')
    
    parser.add_argument('-E', '--n_epochs',
                      dest='n_epochs',
                      type=int,
                      default=300)
    
    parser.add_argument('-l', '--learning_rate',
                      dest='learning_rate',
                      type=float,
                      default=1e-2)
    
    # L1/L2 regularization (search space [1e-5, 1e-3])
    parser.add_argument('-w', '--weight_decay',
                      dest='weight_decay',
                      type=float,
                      default=1e-4)
    
    parser.add_argument('-s', '--smoothing',
                      dest='smoothing',
                      type=float,
                      default=1e-4)
    
    parser.add_argument('-b', '--beta',
                        dest='beta',
                        type=float,
                        default=1.0)
    
    # Kernel functions for radial based interpolation
    parser.add_argument('-k', '--kernel',
                      dest='kernel',
                      type=str,
                      choices=['multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'],
                      #choices=['linear', 'thin_plate_spline', 'cubic', 'quintic', 'multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'],
                      default='gaussian',
                      help='The type of kernel to use for the RBF interpolation.')
    
    parser.add_argument('-e', '--epsilon',
                        dest='epsilon',
                        type=float,
                        default=1.0,
                        help='Epsilon value if kernel is one of: multiquadric, inverse_multiquadric, inverse_quadratic, gaussian.')
        
    return parser.parse_args()



def run_flask(app, socketio, reduced_data):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/data')
    def get_data():
        return jsonify(reduced_data.tolist())
    
    socketio.run(app)


async def main():

    start_time = time.time()

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins='*')
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, OUT_PORT)
    
    args = get_arguments()
    filepath = args.filepath
    filepath_pretrain = args.filepath_pretrain

    if args.optimizer_session:
        params = get_hyperparams_from_log(args.optimizer_session)
        if params:
            n_layers = params['vae']['n_layers']
            activation = get_activation_function(params['vae']['activation'])
            n_epochs = params['vae']['n_epochs']
            learning_rate = params['vae']['learning_rate']
            weight_decay = params['vae']['weight_decay']
            beta = params['vae']['beta']
            smoothing = params['rbf']['smoothing']
            kernel = params['rbf']['kernel']
            epsilon = params['rbf']['epsilon']
    else:
        n_layers = args.n_layers
        activation = args.activation_function
        n_epochs = args.n_epochs
        learning_rate = args.learning_rate
        weight_decay = args.weight_decay
        beta = args.beta
        smoothing = args.smoothing
        kernel = args.kernel
        epsilon = args.epsilon

    try:
        pretrained_model = None
        # pretrain session if a larger context dataset is provided
        if filepath_pretrain is not None:
            loader_pretrain = DataLoader(filepath_pretrain)
            df_pretrain = loader_pretrain.load_presets()
            reducer_pretrain = VectorReducer(df_pretrain, learning_rate, weight_decay, n_layers, activation, beta)
            reducer_pretrain.train_vae(n_epochs)
            pretrained_model = reducer_pretrain.model
        
        # training session on the data that are represented in the 3D virtual space
        loader = DataLoader(filepath)
        df = loader.load_presets()
        original_data = df.drop(['ID', 'name', 'file'], axis=1)

        reducer = VectorReducer(df, learning_rate, weight_decay, n_layers, activation, beta, pretrained_model=pretrained_model)
        reducer.train_vae(n_epochs)
        reduced_data, reconstructed_data = reducer.vae()

        reduced_data = reduced_data[:, 1:] # get rid of ID
        #logging.info(f'Reduced data: {reduced_data}')
        
    
    except FileNotFoundError:
        logging.error('You must provide at least a dataset!')
        exit(1)

    #plot_reconstruction_error(original_data, reduced_data, reconstructed_data)
    end_time = time.time()

    original_data = original_data.values # to np array

    interpolator = RBFInterpolation(reduced_data, original_data, smoothing, kernel, epsilon)
    visualizer = Visualize(reduced_data, app, socketio)
    elapsed_time = end_time - start_time
    logging.info(f"Computation time: {elapsed_time} sec.")
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
    flask_thread.start()

    # Run asyncio event loop
    await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)


if __name__ == '__main__':
    asyncio.run(main())

#TODO:
# 1. check how you drop ID, file and name from csv file