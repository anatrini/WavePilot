import itertools
import numpy as np
import torch

from vae import VectorReducer
from data import DataLoader
from logger import setup_logger
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from torch import nn
from utils import *


logging = setup_logger('Grid Opmization session', file=True)
torch.manual_seed(42)

# Load data
filepath = './data/240207_10presets.json'
loader = DataLoader(filepath)
df = loader.load_presets()


# Set loss function
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
    logging.info(f'Trial {i+1}/{len(param_combinations)}: validation_error = {validation_error}')

    # update best parameters if current model is better
    if validation_error < best_validation_error:
        best_validation_error = validation_error
        best_params = params

# Log the best hypèerparameters and validation error
logging.info(f'Best autoencoder hyperparams: {best_params} with a validation error of {best_validation_error}')


interpolator_grid = {
    'smoothing': np.linspace(0.0, 1.0, num=10),
    'kernel': ['multiquadratic', 'inverse_multiquadratic', 'inverse_quadratic', 'gaussian'],
    'epsilon': np.linspace(0.0, 3.0, num=10)
}

param_combinations = list(itertools.product(*interpolator_grid.values()))

best_validation_distance = float('inf')
best_params = None

# Ottieni tutte le combinazioni di iperparametri per l'interpolatore
param_combinations = list(itertools.product(*interpolator_grid.values()))

best_validation_distance = float('inf')
best_params = None

# Ciclo su tutte le combinazioni di iperparametri per l'interpolatore
for i, params in enumerate(param_combinations):
    # disimballa i parametri
    smoothing, kernel, epsilon = params

    # addestra il modello
    original_data = df.drop(['ID', 'PRESET_NAME'], axis=1)
    original_data = original_data.values
    reduced_data, _ = reducer.autoencoder()
    reduced_data = reduced_data[:, 1:]

    # Addestra l'interpolatore
    interpolator = RBFInterpolator(reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon)
    interpolated_data = interpolator(reduced_data)

    # Stima la distanza euclidea media tra i vettori ridotti e originali
    distances = []
    for original, interpolated in zip(original_data, interpolated_data):
        distance = euclidean(original, interpolated)
        distances.append(distance)

    # Crea l'attributo val_errors per il tracciamento e stima l'errore medio
    validation_distance = np.mean(distances)

    logging.info(f'Trial {i+1}/{len(param_combinations)}: validation_distance = {validation_distance}')

    # aggiorna i migliori parametri se il modello corrente è migliore
    if validation_distance < best_validation_distance:
        best_validation_distance = validation_distance
        best_params = params

# Registra i migliori iperparametri e l'errore di convalida
logging.info(f'Migliori iperparametri dell\'interpolatore: {best_params} con un errore di convalida di {best_validation_distance}')


# # Create a study object from optuna to optimize hyperparameters
# study_interpolator = optuna.create_study(direction='minimize')
# study_interpolator.optimize(objective_interpolator, n_trials=N_TRIALS)
# # Print best params and validation error
# best_trial = study_interpolator.best_trial
# logging.info(f'Best interpolator params {study_interpolator.best_params} with a validation error of {best_trial.value}')