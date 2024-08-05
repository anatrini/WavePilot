import argparse
import itertools
import numpy as np
import torch

from vae_model import VectorReducer
from data import DataLoader
from logger import setup_logger
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split
from utils import *


def get_arguments():
    parser = argparse.ArgumentParser()

    # Small dataset of the presets to be reduced (Mandatory)
    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    # Large dataset of presets to pretrain the model (Optional)
    parser.add_argument('-F', '--filepath_pretrain',
                      dest='filepath_pretrain',
                      type=str,
                      default=None)
    
    # Filepath where to save the pretrained model, only necessary if -F is passed
    parser.add_argument('-s', '--filepath_save_pretrain',
                      dest='filepath_save_pretrain',
                      type=str,
                      default=None)
    
    return parser.parse_args()


logging = setup_logger('Grid Opmization session', file=True)


# Load data
def load_data(filepath):
    loader = DataLoader(filepath)
    return loader.load_presets()


# Compute KL divergence
def kl_divergence(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())


# Calculate validation error
def compute_validation_error(model, criterion, data, beta):
    
    # Drop unnecessary columns
    data = data.drop(columns=['ID', 'name', 'file'])
    data = torch.tensor(data.values).float()

    with torch.no_grad():
        mu, logvar, output = model(data)
        recon_loss = criterion(output, data)
        kl_loss = kl_divergence(mu, logvar)
        mse_loss = (output - data).pow(2).mean()
        loss = (recon_loss + (kl_loss * beta)) + mse_loss
    return loss.item()


def optimize_vae(df_train, df_test, log_prefix, save_pretrained_model=False, save_filepath=None, pretrained_model=None):
    
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
    best_validation_error = float('inf')
    best_params = None
    best_model = None

    # Loop over all combinations of hyperparameters
    for i, params in enumerate(param_combinations):
        try:
            # unpack params
            n_epochs, learning_rate, weight_decay, n_layers, activation_name, beta = params
            activation = get_activation_function(activation_name)

            # train the model
            reducer = VectorReducer(df_train, learning_rate, weight_decay, n_layers, activation, beta, pretrained_model)
            reducer.train_vae(n_epochs)

            # compute validation error
            validation_error = compute_validation_error(reducer.model, reducer.criterion, df_test, beta)
            print(f'{log_prefix} trial {i+1}/{len(param_combinations)}: validation_error = {validation_error}')

            # update best parameters if current model is better
            if validation_error < best_validation_error:
                best_validation_error = validation_error
                best_params = params
                best_model = reducer.model

        except Exception as e:
            logging.error(f'Error during VAE optimization: {e}')
    
    if save_pretrained_model:
        # Save the pretrained model
        torch.save(reducer.model.state_dict(), f'{save_filepath}.pt')
    else:
        # Save best VAE params and log the best hyperparameters and validation error
        logging.info(f'{log_prefix} best VAE hyperparams: {best_params} with a validation error of {best_validation_error}')
    
    return best_params, best_model


def optimize_interpolator(df, reducer, log_prefix):

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
    for i, params in enumerate(param_combinations):
        try:
            # unpack params
            smoothing, kernel, epsilon = params

            # train the model
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
            print(f'{log_prefix} trial {i+1}/{len(param_combinations)}: validation_distance = {validation_distance}')

            if validation_distance < best_validation_distance:
                best_validation_distance = validation_distance
                best_params = params
            
        except Exception as e:
            logging.error(f'Error during interpolation optimization: {e}')

    # Save best VAE params and log the best hyperparameters and validation error
    logging.info(f'{log_prefix} best RBF params: {best_params} with a validation error of {best_validation_distance}')
    return best_params


def main():
    try:
        args = get_arguments()
        torch.manual_seed(42)

        filepath = args.filepath
        filepath_pretrain = args.filepath_pretrain
        filepath_save_pretrain = args.filepath_save_pretrain

        df = load_data(filepath)
        
        df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

        if filepath_pretrain:
            # Optimize and train the VAE to find the best pretrain params
            df_pretrain = load_data(filepath_pretrain)
            df_pretrain_train, df_pretrain_test = train_test_split(df_pretrain, test_size=0.2, random_state=42)

            best_pretrain_params, best_pretrain_model = optimize_vae(df_pretrain_train, df_pretrain_test, 'Pretrain', save_pretrained_model=True, save_filepath=filepath_save_pretrain)

            # Create best pretrain model with the hyperparams found 
            n_epochs, learning_rate, weight_decay, n_layers, activation_name, beta = best_pretrain_params
            activation = get_activation_function(activation_name)
            reducer = VectorReducer(df_pretrain, learning_rate, weight_decay, n_layers, activation, beta)
            reducer.train_vae(n_epochs)

            best_train_params, _ = optimize_vae(df_train, df_test, 'Train', save_pretrained_model=False, save_filepath=None, pretrained_model=best_pretrain_model)

        else:
            best_train_params, _ = optimize_vae(df_train, df_test, 'Train')

        # Train the interpolator with the best train params
        best_rbf_params = optimize_interpolator(df, reducer, 'Interpolator')

    except Exception as e:
        logging.error(f'Error in main: {e}')


if __name__ == '__main__':
    main()










