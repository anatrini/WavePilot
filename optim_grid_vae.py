import itertools
import numpy as np
import torch

from model_vae import VectorReducer
from data import DataLoader
from logger import setup_logger
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from utils import *


logging = setup_logger('Grid Opmization session', file=True)
torch.manual_seed(42)

# Load data
filepath = './data/240207_10presets.json'
loader = DataLoader(filepath)
df = loader.load_presets()


# VAE's params' grid
vae_grid = {
    'n_epochs': [5, 10, 25, 50, 75, 100, 150, 200],
    'learning_rate': np.logspace(-5, -2, num=4),
    'weight_decay': np.logspace(-5, -2, num=4),
    'n_layers': list(range(1, 6)),
    'activation': ['ReLU', 'Sigmoid', 'Tanh'],
    'beta': np.linspace(0.1, 1.0, num=10)
}

# Get all combinations of hyperparameters
param_combinations = list(itertools.product(*vae_grid.values()))

# Compute KL divergence
def kl_divergence(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

def compute_validation_error(model, criterion, data, beta):
    data = data.drop(columns=['ID', 'PRESET_NAME'])
    data = torch.tensor(data.values).float()
    with torch.no_grad():
        mu, logvar, output = model(data)
        recon_loss = criterion(output, data)
        kl_loss = kl_divergence(mu, logvar)
        loss = recon_loss + kl_loss * beta
    return loss.item()

best_validation_error = float('inf')
best_params = None

# Loop over all combinations of hyperparameters
for i, params in enumerate(param_combinations):
    # unpack params
    n_epochs, learning_rate, weight_decay, n_layers, activation_name, beta = params
    activation = get_activation_function(activation_name)

    # train the model
    reducer = VectorReducer(df, learning_rate, weight_decay, n_layers, activation, beta)
    reducer.train_vae(n_epochs)

    # compute validation error
    validation_error = compute_validation_error(reducer.model, reducer.criterion, df, beta)
    print(f'Trial {i+1}/{len(param_combinations)}: validation_error = {validation_error}')

    # update best parameters if current model is better
    if validation_error < best_validation_error:
        best_validation_error = validation_error
        best_params = params


# # Save best VAE params and log the best hyperparameters and validation error
best_vae_params = best_params
logging.info(f'Best VAE hyperparams: {best_vae_params} with a validation error of {best_validation_error}')

# Train the VAE with the best params
n_epochs, learning_rate, weight_decay, n_layers, activation_name, beta = best_vae_params
activation = get_activation_function(activation_name)
reducer = VectorReducer(df, learning_rate, weight_decay, n_layers, activation, beta)
reducer.train_vae(n_epochs)



# Interpolator's params' grid
interpolator_grid = {
    'smoothing': np.linspace(0.001, 1.0, num=10),
    'kernel': ['multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian', 'linear', 'quintic', 'cubic', 'thin_plate_spline'],
    'epsilon': np.linspace(0.0, 3.0, num=30)
}

param_combinations = list(itertools.product(*interpolator_grid.values()))

best_validation_distance = float('inf')
best_params = None

# Loop over all combinations of hyperparameters
param_combinations = list(itertools.product(*interpolator_grid.values()))

best_validation_distance = float('inf')
best_params = None

for i, params in enumerate(param_combinations):
    # unpack params
    smoothing, kernel, epsilon = params

    # train the model
    original_data = df.drop(['ID', 'PRESET_NAME'], axis=1)
    original_data = original_data.values
    reduced_data, _ = reducer.vae()
    reduced_data = reduced_data[:, 1:]
    # train the interpolator
    interpolator = RBFInterpolator(reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon)
    interpolated_data = interpolator(reduced_data)

    # Compute euclidean distance between original and reduced vectors
    distances = []
    for original, interpolated in zip(original_data, interpolated_data):
        distance = euclidean(original, interpolated)
        distances.append(distance)

    validation_distance = np.mean(distances)

    print(f'Trial {i+1}/{len(param_combinations)}: validation_distance = {validation_distance}')

    if validation_distance < best_validation_distance:
        best_validation_distance = validation_distance
        best_params = params

# Save best VAE params and log the best hyperparameters and validation error
best_rbf_params = best_params
logging.info(f'Best RBF params: {best_rbf_params} with a validation error of {best_validation_distance}')