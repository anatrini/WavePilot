import argparse
import asyncio
import time

from vae_model import VectorReducer
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
IN_PORT = 9108 # receive on
OUT_PORT = 9109 # send to


logging = setup_logger('Main VAE')

def get_arguments():
    parser = argparse.ArgumentParser()

    # The actual dataset of the presets to be reduced (Mandatory)
    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    # The pretrained model created on a bigger dataset (Optional)
    parser.add_argument('-p', '--pretrained_model',
                      dest='pretrained_model',
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
                      default=1,
                      help='Set the number of hidden layers used by the model.')
    
    parser.add_argument('-a', '--activation_function',
                      dest='activation_function',
                      type=nn.Module,
                      default=nn.ReLU(),
                      help='Set the activation function used by the model.')
    
    parser.add_argument('-E', '--n_epochs',
                      dest='n_epochs',
                      type=int,
                      default=100)
    
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
    
    parser.add_argument('-b', '--kl_beta',
                        dest='kl_beta',
                        type=float,
                        default=0.05)
    
    parser.add_argument('-m', '--mse_beta',
                        dest='mse_beta',
                        type=float,
                        default=0.1)
    
    # Kernel functions for radial based interpolation
    parser.add_argument('-k', '--kernel',
                      dest='kernel',
                      type=str,
                      choices=['multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'],
                      default='gaussian',
                      help='The type of kernel to use for the RBF interpolation.')
    
    parser.add_argument('-e', '--epsilon',
                        dest='epsilon',
                        type=float,
                        default=1.0,
                        help='Epsilon value if kernel is one of: multiquadric, inverse_multiquadric, inverse_quadratic, gaussian.')
    
    parser.add_argument('-d', '--degree',
                        dest='degree',
                        type=int,
                        default=None,
                        help='Degree of the added polynomial. Minimum degree for RBFs: multiquadric=0, linear=0, thin_plate_spline=1, cubic=1, quintic=2. The default value is the minimum degree for kernel or 0 if there is no minimum degree. Set this to -1 for no added polynomial.')
        
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
    pretrained_model = args.pretrained_model

    if args.optimizer_session:
        params = get_hyperparams_from_log(args.optimizer_session)
        n_layers = params['vae']['n_layers']
        activation = get_activation_function(params['vae']['activation_function'])
        n_epochs = params['vae']['num_epochs']
        learning_rate = params['vae']['learning_rate']
        weight_decay = params['vae']['weight_decay']
        kl_beta = params['vae']['kl_beta']
        mse_beta = params['vae']['mse_beta']
        smoothing = params['rbf']['smoothing']
        kernel = params['rbf']['kernel']
        epsilon = params['rbf']['epsilon']
        degree = params['rbf']['degree']
    else:
        n_layers = args.n_layers
        activation = args.activation_function
        n_epochs = args.n_epochs
        learning_rate = args.learning_rate
        weight_decay = args.weight_decay
        kl_beta = args.kl_beta
        mse_beta = args.mse_beta
        smoothing = args.smoothing
        kernel = args.kernel
        epsilon = args.epsilon
        degree = args.degree

    try:
        loader = DataLoader(filepath)
        df = loader.load_presets()
        
        if pretrained_model is not None:
            pmodel = torch.load(pretrained_model)
            reducer = VectorReducer(df, learning_rate, weight_decay, n_layers, activation, kl_beta, mse_beta, pretrained_model=pmodel)
        else:
            reducer = VectorReducer(df, learning_rate, weight_decay, n_layers, activation, kl_beta, mse_beta)

        reducer.train_vae(n_epochs)
        reduced_data, reconstructed_data = reducer.vae()
        
    except FileNotFoundError:
        logging.error('You must provide at least a dataset!')
        exit(1)

    original_data = df.values # to np array
    # Uncomment the line below to plot the reconstruction error
    #plot_reconstruction_error(original_data, reduced_data, reconstructed_data)

    interpolator = RBFInterpolation(reduced_data, original_data, smoothing, kernel, epsilon, degree)
    visualizer = Visualize(reduced_data, app, socketio)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Computation time: {elapsed_time} sec.")
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
    flask_thread.start()

    # Run asyncio event loop
    await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)


if __name__ == '__main__':
    asyncio.run(main())