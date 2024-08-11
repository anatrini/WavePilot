import numpy as np
import pandas as pd

#import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler

import torch
from torch import nn


# Read and get best hyperparams from log session
def get_hyperparams_from_log(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    params = {}
    for line in lines:
        if "Best VAE hyperparams" in line:
            # Get autoencoder's best hyperp fomr log
            params_str = line.split("Best VAE hyperparams: ")[1].split(" with")[0]
            params_tuple = eval(params_str)
            params['vae'] = {'n_epochs': params_tuple[0], 'learning_rate': params_tuple[1], 'weight_decay': params_tuple[2], 'n_layers': params_tuple[3], 'activation': params_tuple[4], 'beta': params_tuple[5]}
        elif "Best RBF params" in line:
            # Get interpolator's best hyperp fomr log
            params_str = line.split("Best RBF params: ")[1].split(" with")[0]
            params_tuple = eval(params_str)
            params['rbf'] = {'smoothing': params_tuple[0], 'kernel': params_tuple[1], 'epsilon': params_tuple[2], 'degree': params_tuple[3]}

    return params

# Get activation function module from string
def get_activation_function(activation_name):
    activation_functions = {
        'ReLU': nn.ReLU(),
        'Sigmoid': nn.Sigmoid(),
        'Tanh': nn.Tanh()
    }
    return activation_functions.get(activation_name, None)


# Compute loss for optimization
def compute_validation_error(model, criterion, val_data):
    with torch.no_grad():
        val_data = val_data.drop(['ID', 'PRESET_NAME'], axis=1)
        val_data = torch.tensor(val_data.values).float()
        _, output = model(val_data)
        loss = criterion(output, val_data)
    return loss.item()

def select_random_entries(input_csv, ouput_csv, n):
    df = pd.read_csv(input_csv)
    df['ID'] = range(1, len(df) + 1)
    df.to_csv(input_csv, index=False)

    df_sample = df.sample(n)
    df_sample.to_csv(ouput_csv, index=False)


def plot_reconstruction_error(original_data, reduced_data, reconstructed_data):
    reconstruction_error = np.mean(np.square(original_data - reconstructed_data), axis=1)
    average_error = np.mean(reconstruction_error)
    print(average_error)

    # Estrai le coordinate x, y, z dai dati ridotti
    x, y, z = reduced_data.T

    # Crea un grafico a dispersione 3D dell'errore di ricostruzione
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                   marker=dict(size=5, color=reconstruction_error, colorscale='Viridis'))])

    fig.update_layout(title='3D Scatter Plot of Reconstruction Error',
                  scene=dict(xaxis_title='X',
                             yaxis_title='Y',
                             zaxis_title='Reconstruction Error'))
    fig.show()