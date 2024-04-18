import numpy as np
import optuna
import torch

from model_ae import VectorReducer
from data import DataLoader
from logger import setup_logger
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import KFold, train_test_split
from torch import nn
from utils import *


logging = setup_logger('Random Opmization session', file=True)
torch.manual_seed(42)

N_TRIALS = 100

# Load data
filepath = './data/240207_5presets.json'
loader = DataLoader(filepath)
df = loader.load_presets()
# Train test split data
train_data, val_data = train_test_split(df, test_size=0.2)

# Set fold number for cross validation
n_splits = 2
kf = KFold(n_splits=n_splits)

# Set loss function
criterion = nn.MSELoss()

def objective_autoencoder(trial):
    n_epochs = trial.suggest_categorical('n_epochs', [5, 10, 25, 50, 75, 100, 150, 200])
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True)
    weight_decay = trial.suggest_float('weight_decay', 1e-5, 1e-2, log=True)
    n_layers = trial.suggest_int('n_layers', 1, 5)
    activation_name = trial.suggest_categorical('activation', ['ReLU', 'Sigmoid', 'Tanh'])
    activation = get_activation_function(activation_name)

    # Init validation error and evaluate cross validation
    validation_errors = []
    for train_index, val_index in kf.split(train_data):
        train_fold = train_data.iloc[train_index]

        reducer = VectorReducer(train_fold, learning_rate, weight_decay, n_layers, activation)
        reducer.train_autoencoder(n_epochs)

        val_fold = train_data.iloc[val_index]
        val_error = compute_validation_error(reducer.model, reducer.criterion, val_fold)
        validation_errors.append(val_error)

    # Create val errors attribute for plotting and estimate avg error 
    trial.set_user_attr('validation_errors', validation_errors)
    validation_error = np.mean(validation_errors)
    return validation_error


# Create a study object from optuna to optimize hyperparameters
study_autoencoder = optuna.create_study(direction='minimize')
study_autoencoder.optimize(objective_autoencoder, n_trials=N_TRIALS)

# Print best params and validation error
best_trial = study_autoencoder.best_trial
logging.info(f'Best autoencoder hyperparams: {study_autoencoder.best_params} with a validation error of {best_trial.value}')

# Train a new model with the best hyperparams
best_params = study_autoencoder.best_params
n_epochs = best_params['n_epochs']
learning_rate = best_params['learning_rate']
weight_decay = best_params['weight_decay']
n_layers = best_params['n_layers']
activation_name = best_params['activation']
activation = get_activation_function(activation_name)


def objective_interpolator(trial):
    smoothing = trial.suggest_float('smoothing', 0.0, 1.0)
    #kernel = trial.suggest_categorical('kernel', ['linear', 'thin_plate_spline', 'cubic', 'quintic', 'multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'])
    kernel = trial.suggest_categorical('kernel', ['multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'])
    epsilon = trial.suggest_float('epsilon', 0.0, 3.0)

    original_data = train_data.drop(['ID', 'PRESET_NAME'], axis=1)
    original_data = original_data.values
    reducer = VectorReducer(train_data, learning_rate, weight_decay, n_layers, activation)
    reducer.train_autoencoder(n_epochs)
    reduced_data, _ = reducer.autoencoder()
    reduced_data = reduced_data[:, 1:]

    # Train interpolator
    interpolator = RBFInterpolator(reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon)
    interpolated_data = interpolator(reduced_data)

    # Estimate average euclidean distance between reduced and original vectors
    distances = []
    for original, interpolated in zip(original_data, interpolated_data):
        distance = euclidean(original, interpolated)
        distances.append(distance)

    # Create val errors attribute for plotting and estimate avg error 
    validation_distance = np.mean(distances)

    return validation_distance


# Create a study object from optuna to optimize hyperparameters
study_interpolator = optuna.create_study(direction='minimize')
study_interpolator.optimize(objective_interpolator, n_trials=N_TRIALS)
# Print best params and validation error
best_trial = study_interpolator.best_trial
logging.info(f'Best interpolator params {study_interpolator.best_params} with a validation error of {best_trial.value}')