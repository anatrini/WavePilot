import numpy as np
import optuna
import torch

from autoencoder import VectorReducer
from data import DataLoader
from logger import setup_logger 
from sklearn.model_selection import KFold, train_test_split
from torch import nn


logging = setup_logger('Opmization session')
torch.manual_seed(42)


def compute_validation_error(autoencoder, criterion, val_data):
    #print(val_data)
    val_data = val_data.drop(['ID', 'PRESET_NAME'], axis=1)
    val_data = torch.tensor(val_data.values).float()
    reconstructed_data = autoencoder(val_data)
    error = criterion(reconstructed_data, val_data)
    return error.item()


# Load data
filepath = './data/240108_1_test.json'
loader = DataLoader(filepath)
df = loader.load_presets()
#df_data = df.drop(['ID', 'PRESET_NAME'], axis=1)

train_data, val_data = train_test_split(df, test_size=0.2)

# Set fold number for cross validation
n_splits = 5
kf = KFold(n_splits=n_splits)

# Set loss function
criterion = nn.MSELoss()

def objective(trial):
    num_epochs = trial.suggest_categorical('num_epochs', [5, 10, 25, 50, 75, 100, 150, 200])
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True)
    weight_decay = trial.suggest_float('weight_decay', 1e-5, 1e-3, log=True)

    # Init validation error
    validation_error = 0
    # Cross validate
    for train_index, val_index in kf.split(train_data):
        train_fold = train_data.iloc[train_index]
        val_fold = train_data.iloc[val_index]

        reducer = VectorReducer(train_fold, learning_rate, weight_decay)
        reducer.train_autoencoder(num_epochs)

        val_error = compute_validation_error(reducer.model, reducer.criterion, val_fold)
        validation_error += val_error

    # Estimate avg error   
    validation_error /= n_splits
    return validation_error


# Create a study object from optuna to optimize hyperparameters
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=200)

# Print best params
logging.info(f'Best hyperparams: {study.best_params}.')

# Train a new model with the best hyperparams on the entire data
best_params = study.best_params
num_epochs = best_params['num_epochs']
learning_rate = best_params['learning_rate']
weight_decay = best_params['weight_decay']

reducer = VectorReducer(train_data, learning_rate, weight_decay)
reducer.train_autoencoder(num_epochs)

# # Estimate reconstruction error
test_error = compute_validation_error(reducer.model, reducer.criterion, val_data)
logging.info(f'Test error: {test_error}.')