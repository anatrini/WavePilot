import numpy as np
import optuna
import torch

from autoencoder import VectorReducer
from data import DataLoader
from logger import setup_logger
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import KFold, train_test_split
from torch import nn


logging = setup_logger('Opmization session', file=True)
torch.manual_seed(42)

N_TRIALS = 100

def compute_validation_error(autoencoder, criterion, val_data):
    #print(val_data)
    val_data = val_data.drop(['ID', 'PRESET_NAME'], axis=1)
    val_data = torch.tensor(val_data.values).float()
    reconstructed_data = autoencoder(val_data)
    error = criterion(reconstructed_data, val_data)
    return error.item()


# Load data
filepath = './data/240120_test.json'
loader = DataLoader(filepath)
df = loader.load_presets()
# Train test split data
train_data, val_data = train_test_split(df, test_size=0.2)

# Set fold number for cross validation
n_splits = 5
kf = KFold(n_splits=n_splits)

# Set loss function
criterion = nn.MSELoss()

def objective_autoencoder(trial):
    num_epochs = trial.suggest_categorical('num_epochs', [5, 10, 25, 50, 75, 100, 150, 200])
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True)
    weight_decay = trial.suggest_float('weight_decay', 1e-5, 1e-2, log=True)

    # Init validation error and evaluate cross validation
    validation_errors = []
    for train_index, val_index in kf.split(train_data):
        train_fold = train_data.iloc[train_index]
        val_fold = train_data.iloc[val_index]

        reducer = VectorReducer(train_fold, learning_rate, weight_decay)
        reducer.train_autoencoder(num_epochs)

        val_error = compute_validation_error(reducer.model, reducer.criterion, val_fold)
        validation_errors.append(val_error)

    # Estimate avg error   
    validation_error = np.mean(validation_errors)
    return validation_error


# Create a study object from optuna to optimize hyperparameters
study_autoencoder = optuna.create_study(direction='minimize')
study_autoencoder.optimize(objective_autoencoder, n_trials=N_TRIALS)

# Print best params
logging.info(f'Best autoencoder hyperparams: {study_autoencoder.best_params}.')

# Train a new model with the best hyperparams
best_params = study_autoencoder.best_params
num_epochs = best_params['num_epochs']
learning_rate = best_params['learning_rate']
weight_decay = best_params['weight_decay']


def objective_interpolator(trial):
    smoothing = trial.suggest_float('smoothing', 0.0, 1.0)
    kernel = trial.suggest_categorical('kernel', ['linear', 'thin_plate_spline', 'cubic', 'quintic', 'multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian'])
    epsilon = trial.suggest_float('epsilon', 0.0, 3.0)

    original_data = train_data.drop(['ID', 'PRESET_NAME'], axis=1)
    original_data = original_data.values
    reducer = VectorReducer(train_data, learning_rate, weight_decay)
    reducer.train_autoencoder(num_epochs)
    reduced_data = reducer.autoencoder()
    reduced_data = reduced_data[:, 1:]

    # Train interpolator
    interpolator = RBFInterpolator(reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon)
    interpolated_data = interpolator(reduced_data)
    #print(f'Or data {original_data}')
    #print(f'Interp data {interpolated_data}')

    # Estimate average euclidena distance between reduced and original vectors
    errors = []
    for original, interpolated in zip(original_data, interpolated_data):
        distance = euclidean(original, interpolated)
        errors.append(distance)

    # # Estimate average validation error
    validation_error = np.mean(errors)

    return validation_error


# Create a study object from optuna to optimize hyperparameters
study_interpolator = optuna.create_study(direction='minimize')
study_interpolator.optimize(objective_interpolator, n_trials=N_TRIALS)

# Print best params
logging.info(f'Best interpolator params {study_interpolator.best_params}')