import argparse
import asyncio

from autoencoder import VectorReducer
from data import DataLoader
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from interpolator import RBFInterpolation
from pythonosc import udp_client
from threading import Thread
from visualizer import Visualize


IP_ADDRESS = '127.0.0.1'
IN_PORT = 5105
OUT_PORT = 5106


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    parser.add_argument('-E', '--num_epochs',
                      dest='num_epochs',
                      type=int,
                      default=100)
    
    parser.add_argument('-l', '--learning_rate',
                      dest='learning_rate',
                      type=float,
                      default=1e-3)
    
    # L1/L2 regularization (search space [1e-5, 1e-3])
    parser.add_argument('-w', '--weight_decay',
                      dest='weight_decay',
                      type=float,
                      default=1e-3)
    
    # Kernel functions for radial based interpolation
    parser.add_argument('-k', '--kernel',
                      dest='kernel',
                      type=str,
                      choices=['linear', 'thin_plate_spline', 'cubic', 'quintic', 'multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'],
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

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins='*')
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, OUT_PORT)
    
    args = get_arguments()
    filepath = args.filepath
    num_epochs = args.num_epochs
    learning_rate = args.learning_rate
    weight_decay = args.weight_decay
    kernel = args.kernel
    epsilon = args.epsilon

    loader = DataLoader(filepath)
    df = loader.load_presets()
    original_data = df.drop(['ID', 'PRESET_NAME'], axis=1)

    reducer = VectorReducer(df, learning_rate, weight_decay)
    reducer.train_autoencoder(num_epochs)
    reduced_data = reducer.autoencoder()
    print(f'Reduced data {reduced_data[:, 1:]}') # togli l'ID
    print(f'Original data {original_data.values}') # trasformalo da dataframe e numpy e togli l'ID

    interpolator = RBFInterpolation(reduced_data, original_data, kernel, epsilon)
    visualizer = Visualize(reduced_data, app, socketio)
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, args=(app, socketio, reduced_data))
    flask_thread.start()

    # Run asyncio event loop
    await visualizer.run(IP_ADDRESS, IN_PORT, interpolator, osc_client)


if __name__ == '__main__':
    asyncio.run(main())