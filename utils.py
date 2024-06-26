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
            params['rbf'] = {'smoothing': params_tuple[0], 'kernel': params_tuple[1], 'epsilon': params_tuple[2]}

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


# Plot autoencoder e interpolator performances during optimization
def plot_losses(model_trials, interpolator_trials):
    model_errors = []
    interpolator_errors = []

    for trial in model_trials:
        #model_errors.append(trial.user_attrs['validation_errors'])
        model_errors.append(trial.value)
    for trial in interpolator_trials:
        interpolator_errors.append(trial.value)

    # Create plot
    fig = make_subplots(rows=1, cols=2)
    # Add traces to the plot
    fig.add_trace(go.Scatter(y=model_errors, mode='lines', name=f'Autoencoder metrics'), row=1, col=1)
    fig.add_trace(go.Scatter(y=interpolator_errors, mode='lines', name=f'Interpolator metrics'), row=1, col=2)

    fig.update_layout(height=600, width=1200, title='Metrics during optimization')
    fig.update_xaxes(title_text='Trials', row=1, col=1)
    fig.update_yaxes(title_text='Target', row=1, col=1)
    fig.update_xaxes(title_text='Trials', row=1, col=2)
    fig.update_yaxes(title_text='Target', row=1, col=2)
    fig.show()


def plot_euclidean_distance(df_original, data_reduced):
    # df_original is a Dataset, data_reduced is np array
    dist_original = distance.pdist(df_original.values, 'euclidean')
    # data_reduced is not normalized like the original data so we have to scale it
    scaler = MinMaxScaler()
    data_reduced_norm = scaler.fit_transform(data_reduced)
    dist_reduced = distance.pdist(data_reduced_norm, 'euclidean')
    distances = np.array([distance.euclidean(a, b) for a, b in zip(df_original.values, data_reduced_norm)])

    fig = go.Figure(data=go.Scatter(x=dist_original, y=dist_reduced, mode='markers',
                                    marker=dict(color=distances, colorscale='Viridis', size=8,
                                    colorbar=dict(title='Euclidean distances between original and reconstructed vectors'))))
    
    fig.update_layout(title=f'Correlation between orginal and reconstructed vectors\'s distances.',
                      xaxis_title='Original distances',
                      yaxis_title='Reconstructed distances'
                      )
    fig.show()


def plot_dispersion_matrix(original_data, reconstructed_data):
    df_original = pd.DataFrame(original_data)
    df_reconstructed = pd.DataFrame(reconstructed_data)

    # Crea una matrice di dispersione per i dati originali
    fig1 = go.Figure(data=go.Splom(dimensions=[dict(label=col, values=df_original[col]) for col in df_original.columns]))
    fig1.update_layout(title='Scatter Matrix of Original Data')
    fig1.show()

    # Crea una matrice di dispersione per i dati ricostruiti
    fig2 = go.Figure(data=go.Splom(dimensions=[dict(label=col, values=df_reconstructed[col]) for col in df_reconstructed.columns]))
    fig2.update_layout(title='Scatter Matrix of Reconstructed Data')
    fig2.show()

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


def plot_average_reconstruction_error(datasets):
    # Calcola l'errore di ricostruzione medio per ciascun dataset
    average_errors = []
    for original_data, reduced_data, reconstructed_data in datasets:
        reconstruction_error = np.mean(np.square(original_data - reconstructed_data), axis=1)
        average_error = np.mean(reconstruction_error)
        average_errors.append(average_error)

    # Crea un grafico a barre dell'errore di ricostruzione medio
    fig = go.Figure(data=[go.Bar(x=['2', '5', '10', '20', '30', '50', '100'],  # Aggiungi le dimensioni dei tuoi dataset qui
                           y=average_errors)])

    fig.update_layout(title='Average Reconstruction Error for Different Datasets',
                      xaxis_title='Dataset',
                      yaxis_title='Average Reconstruction Error')
    fig.show()

#TODO:
# 1. polish utils (get rid of unused defs)