import argparse
import itertools
from logging import Logger
from logging.handlers import QueueListener
from multiprocessing import Manager, Pool, Process, cpu_count

import numpy as np
import torch
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from data import DataLoader
from logger import setup_logger
from model import VectorReducer
from utils import get_activation_function

RANDOM_SEED = 579


def get_arguments():
    parser = argparse.ArgumentParser()

    # (Small) dataset of the presets to be reduced (Mandatory)
    parser.add_argument('-f', '--filepath',
                        dest='filepath',
                        type=str,
                        required=True,
                        help='Dataset of the presets to be reduced.')

    parser.add_argument('-n', '--num_entries',
                        dest='num_entries',
                        type=int,
                        default=None,
                        help='Number of random entries to select from the dataset.')

    # Large dataset of presets to pretrain the model (Optional)
    parser.add_argument('-F', '--filepath_pretrain_dataset',
                        dest='filepath_pretrain_dataset',
                        type=str,
                        default=None,
                        help='Large dataset to pretrain the model.')
    
    # Pretrained model of presets of the large dataset (Optional)
    parser.add_argument('-p', '--filepath_pretrained_model',
                        dest='filepath_pretrained_model',
                        type=str,
                        default=None,
                        help='Path to a pre-trained model (.pt) to be loaded instead of recalculating it.')

    # Filepath where to save the pretrained model, only necessary if -F is passed
    parser.add_argument('-s', '--filepath_save_pretrain',
                        dest='filepath_save_pretrain',
                        type=str,
                        default=None)

    parser.add_argument('-d', '--disable_split',
                        dest='disable_split',
                        action='store_false',
                        help='Disable train/test split and use the entire dataset for both training and validation. Default split enabled.')
    
    # Masked parameters
    parser.add_argument('-m', '--mask_columns',
                        dest='mask_columns',
                        type=str,
                        nargs='+',  # Permette di passare una lista di stringhe
                        default=None,
                        help='List of parameter names to be masked (excluded) from the dataset.')

    return parser.parse_args()



log_progress: Logger = setup_logger('ProgressLogger', file=False)

# Load data
def load_data(filepath, num_entries=None, mask_columns=None):
    loader = DataLoader(filepath, mask_columns)
    df = loader.load_presets()

    if num_entries:
        np.random.seed(RANDOM_SEED)
        selected_idx = np.random.choice(df.shape[0], size=num_entries, replace=False)
        df = df[selected_idx]
        # df = df[np.random.choice(df.shape[0], size=num_entries, replace=False)]
        log_progress.info("Randomly selected %d entries from the dataset", num_entries)
        log_progress.info("Selected indices from dataset: %s", selected_idx)
    else:
        log_progress.info("Using the entire dataset!")

    return df


# Compute KL divergence
def kl_divergence(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())


# Calculate validation error
def compute_validation_error(reducer, data):
    data_tensor = torch.tensor(data).float().to(reducer.device)
    with torch.no_grad():
        return reducer.compute_loss(data_tensor, compute_gradients=False)



# Progress listener process
def progress_listener(queue, total):
    with tqdm(total=total) as pbar:
        while True:
            msg = queue.get()
            if msg == 'DONE':
                break
            pbar.update(1)


def log_listener(log_queue, handlers):
    listener = QueueListener(log_queue, *handlers)
    listener.start()
    return listener



def train_and_validate(queue, n_epochs, params, original_train, original_test, pretrained_model=None):
    try:
        # unpack params
        learning_rate, weight_decay, n_layers, layer_dim, activation_name, kl_beta, mse_beta = params
        activation = get_activation_function(activation_name)

        # Initialize the model
        reducer = VectorReducer(
                                original_train,
                                learning_rate,
                                weight_decay,
                                n_layers,
                                layer_dim,
                                activation,
                                kl_beta,
                                mse_beta,
                                pretrained_model)

        # Train the model
        reducer.train_vae(n_epochs)

        # Validate the model
        validation_error = compute_validation_error(reducer, original_test)

        # Move the model to cpu
        reducer.move_to_cpu()

        return validation_error, params, reducer.model

    except Exception as e:
        log_progress.error("Error during VAE optimization: %s", e)
        return float('inf'), params, None  # Ritorna un valore alto per continuare l'ottimizzazione
    finally:
        queue.put(1) # Notify progress


def interpolate_and_validate(progress_queue, params, original_data, reduced_data, min_degree, fixed_epsilon_kernels):
    try:
        # Unpack parameters
        smoothing, kernel, epsilon, degree = params

        # Skip epsilon for certain kernels
        if kernel in fixed_epsilon_kernels:
            epsilon = 1.0

        # Ensure degree meets minimum requirements for certain kernels
        if kernel in min_degree and degree < min_degree[kernel]:
            log_progress.warning("Skipping configuration: kernel=%s, degree=%d (below minimum degree requirement)", kernel, degree)
            progress_queue.put(1)
            return float('inf'), params  # Invalid configuration

        # Calculate the number of polynomial terms for the given degree
        num_poly_terms = 0 if degree == -1 else (degree + 1) * (degree + 2) // 2
        if original_data.shape[0] < num_poly_terms:
            log_progress.warning("Skipping configuration: insufficient dataset size for degree=%d (requires %d entries)", degree, num_poly_terms)
            progress_queue.put(1)
            return float('inf'), params

        interpolator = RBFInterpolator(
                                        reduced_data,
                                        original_data,
                                        smoothing=smoothing,
                                        kernel=kernel,
                                        epsilon=epsilon,
                                        degree=degree)

        # Validate interpolator
        interpolated_data = interpolator(reduced_data)
        distances = [
                    euclidean(original, interpolated)
                    for original, interpolated in zip(original_data, interpolated_data)]
        validation_distance = np.mean(distances)

        # Log progress
        log_progress.info("Configuration validated: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f, validation_distance=%.5f", kernel, degree, smoothing, epsilon, validation_distance)
        progress_queue.put(1)

        return validation_distance, params

    except np.linalg.LinAlgError:
        # Handle singular matrix error
        log_progress.warning("Skipping configuration due to singular matrix error: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f", kernel, degree, smoothing, epsilon)
        progress_queue.put(1)
        return float('inf'), params

    except ValueError as e:
        # Handle specific ValueError for minimum data points
        if "At least" in str(e):
            log_progress.warning("Skipping configuration due to insufficient data points: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f", kernel, degree, smoothing, epsilon)
            progress_queue.put(1)
            return float('inf'), params
        else:
            raise e

    except Exception as e:
        # Handle any other exceptions
        log_progress.error("Unexpected error in interpolate_and_validate: %s", e)
        progress_queue.put(1)
        return float('inf'), params



def optimize_vae(df_train, df_test, log_prefix, save_pretrained_model=False, save_filepath=None, pretrained_model=None):

    # VAE's params' grid
    vae_grid = {
        'n_epochs': [50, 100, 200],
        'learning_rate': np.logspace(-6, -2, num=5),
        'weight_decay': np.logspace(-6, -2, num=5),
        'n_layers': list(range(1, 4)),
        'layer_dim': [64, 128, 256],
        'activation': ['ReLU', 'LeakyReLU', 'ELU', 'GELU'],
        'kl_beta': np.linspace(0.01, 1.0, num=5),
        'mse_beta': np.linspace(0.1, 2.0, num=5)
    }

    # vae_grid = {
    #     'n_epochs': [50, 100],
    #     'learning_rate': np.logspace(-6, -2, num=2),
    #     'weight_decay': np.logspace(-6, -2, num=2),
    #     'n_layers': list(range(1, 2)),
    #     'layer_dim': [64, 128],
    #     'activation': ['ELU', 'GELU'],
    #     'kl_beta': np.linspace(0.01, 1.0, num=4),
    #     'mse_beta': np.linspace(0.1, 2.0, num=4)
    # }

    # Get all combinations of hyperparameters
    param_combinations = list(itertools.product(*vae_grid.values()))
    total_combinations = len(param_combinations)

    # Logger configurations
    manager = Manager()
    progress_queue = manager.Queue()
    log_queue = manager.Queue()

    log = setup_logger('OptimizationLogger', log_queue=log_queue, file=True)
    listener_log = log_listener(log_queue, log.handlers)

    # Progress listener
    listener_process = Process(target=progress_listener, args=(progress_queue, total_combinations))
    listener_process.start()

    try:
        log_progress.info("%s Starting VAE optimization...", log_prefix)

        input_data = [(progress_queue, params[0], params[1:], df_train, df_test, pretrained_model)
                      for params in param_combinations]

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(train_and_validate, input_data)

        # Sort all combinations by validation error
        sorted_results = sorted(results, key=lambda x: x[0])
        top_500_results = sorted_results[:500]  
        
        # Select only the best combination
        best_validation_error, best_params_tuple, best_model = top_500_results[0]

        # Find the index of the best combination in the original results
        best_idx = results.index(top_500_results[0])
        num_epochs = input_data[best_idx][1]

        # Create the dictionary of the best parameters
        best_params = {
            'num_epochs': num_epochs,
            "learning_rate": best_params_tuple[0],
            "weight_decay": best_params_tuple[1],
            "n_layers": best_params_tuple[2],
            "layer_dim": best_params_tuple[3],
            "activation_function": best_params_tuple[4],
            "kl_beta": best_params_tuple[5],
            "mse_beta": best_params_tuple[6]
        }

        log_progress.info("%s Best Validation Error: %.12f | Params: %s", log_prefix, best_validation_error, best_params)


        for idx, (validation_error, params_tuple, _) in enumerate(top_500_results):  
            best_idx = results.index((validation_error, params_tuple, _))
            num_epochs = input_data[best_idx][1]  

            param_dict = {
                'num_epochs': num_epochs,
                "learning_rate": params_tuple[0],
                "weight_decay": params_tuple[1],
                "n_layers": params_tuple[2],
                "layer_dim": params_tuple[3],
                "activation_function": params_tuple[4],
                "kl_beta": params_tuple[5],
                "mse_beta": params_tuple[6],
                "validation_error": validation_error
            }

            log.info(param_dict) 

    except Exception as e:
        log_progress.error("%s Error during optimization: %s", log_prefix, e)
        raise

    finally:
        progress_queue.put('DONE')
        listener_process.join()
        log_queue.put(None)
        listener_log.stop()

    log.info("Best VAE hyperparams: %s with a validation error of %.12f", best_params, best_validation_error)

    if save_pretrained_model:
        torch.save(best_model, f'{save_filepath}.pt')

    return best_params, best_model



def optimize_interpolator(original_data, reduced_data, log_prefix):

    # Interpolator's params' grid
    interpolator_grid = {
        'smoothing': np.linspace(0.0, 1.0, num=10),
        'kernel': ['multiquadric', 'inverse_multiquadric', 'inverse_quadratic', 'gaussian', 'linear', 'quintic', 'cubic', 'thin_plate_spline'],
        'epsilon': np.linspace(1e-03, 3.0, num=10),
        'degree': np.linspace(-1, 2, num=4, dtype=int)
    }

    # Minimum degree requirements for each kernel
    min_degree = {
        'multiquadric': 0,
        'linear': 0,
        'thin_plate_spline': 1,
        'cubic': 1,
        'quintic': 2
    }

    # Kernels for which epsilon should be set to 1
    fixed_epsilon_kernels = ['linear', 'thin_plate_spline', 'cubic', 'quintic']

    param_combinations = list(itertools.product(*interpolator_grid.values()))
    total_combinations = len(param_combinations)

    # Logger setup
    manager = Manager()
    progress_queue = manager.Queue()
    log_queue = manager.Queue()

    log = setup_logger('OptimizationLogger', log_queue=log_queue, file=True)
    listener_log = log_listener(log_queue, log.handlers)

    # Listener for progress
    listener_process = Process(target=progress_listener, args=(progress_queue, total_combinations))
    listener_process.start()

    try:
        log_progress.info("%s Starting interpolator optimization with %d combinations", log_prefix, total_combinations)

        input_data = [(progress_queue, params, original_data, reduced_data, min_degree, fixed_epsilon_kernels)
                      for params in param_combinations]

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(interpolate_and_validate, input_data)

        # **Select the 500 best combinations based on validation distance**
        top_500_results = sorted(results, key=lambda x: x[0])[:500]

        # **Retrieve the best parameters**
        best_validation_distance, best_params_tuple = top_500_results[0]

        best_params = {
            'smoothing': best_params_tuple[0],
            'kernel': best_params_tuple[1],
            'epsilon': best_params_tuple[2],
            'degree': best_params_tuple[3]
        }


        for validation_distance, params_tuple in top_500_results:
            param_dict = {
                'smoothing': params_tuple[0],
                'kernel': params_tuple[1],
                'epsilon': params_tuple[2],
                'degree': params_tuple[3],
                'validation_distance': validation_distance
            }
            log.info(param_dict)  # ✅ Logs all 500 best interpolator results

    except Exception as e:
        log_progress.error("%s Error during interpolator optimization: %s", log_prefix, e)
        raise

    finally:
        progress_queue.put('DONE')
        listener_process.join()
        log_queue.put(None)
        listener_log.stop()

    log.info("%s Best Interpolator params: %s with a validation distance of %.12f", log_prefix, best_params, best_validation_distance)

    return best_params



def pretrain_and_train(filepath_pretrain, filepath_save_pretrain, df_train, df_test):
    """Performs pretraining on a large dataset and then training on a smaller one."""

    # Load the pretraining dataset
    df_pretrain = load_data(filepath_pretrain)
    df_train_pretrain, df_test_pretrain = train_test_split(df_pretrain, test_size=0.3, random_state=12)

    # Optimise VAE on the pretraining dataset
    best_params_pretrain, best_model_pretrain = optimize_vae(df_train_pretrain, df_test_pretrain, 'Pretrain', save_pretrained_model=True, save_filepath=filepath_save_pretrain)

    # Call run_training() for pretraining on df_train_pretrain
    run_training(best_params_pretrain, df_train_pretrain, None)  # No pre-trained model for the first phase

    # Train using the pre-trained model
    best_params_train, _ = optimize_vae(df_train, df_test, 'Train', pretrained_model=best_model_pretrain)

    reduced_data, reconstructed_data = run_training(best_params_train, df_train, best_model_pretrain)
    return reduced_data, reconstructed_data


def train_with_pretrained_model(filepath_model, df_train, df_test):
    """Refines training using an already pre-trained model, following the original main."""
    
    # Load the pre-trained model
    pretrained_model = torch.load(filepath_model)

    # Execute training using the pre-trained model
    best_params_train, _ = optimize_vae(df_train, df_test, 'Train', pretrained_model=pretrained_model)

    # Execute final training
    reduced_data, reconstructed_data = run_training(best_params_train, df_train, pretrained_model)
    return reduced_data, reconstructed_data


def train_from_scratch(df_train, df_test):
    """Performs standard training without pretraining or pre-trained models."""
    
    # Optimise VAE from scratch
    best_params_train, _ = optimize_vae(df_train, df_test, 'Train')

    # Execute final training
    reduced_data, reconstructed_data = run_training(best_params_train, df_train, None)
    return reduced_data, reconstructed_data


def run_training(best_params_train, df_train, pretrained_model):
    """Executes training with the best parameters found."""
    
    best_params_train = {
        key: float(value) if key != "activation_function" and isinstance(value, str) else value
        for key, value in best_params_train.items()
    }

    reducer_train = VectorReducer(
        df_train,
        best_params_train["learning_rate"],
        best_params_train["weight_decay"],
        best_params_train["n_layers"],
        best_params_train["layer_dim"],
        get_activation_function(best_params_train["activation_function"]),
        best_params_train["kl_beta"],
        best_params_train["mse_beta"],
        pretrained_model=pretrained_model
    )

    reducer_train.train_vae(best_params_train["num_epochs"])
    return reducer_train.vae()



def main():
    try:
        args = get_arguments()
        torch.manual_seed(42)

        # Load the main dataset
        df = load_data(args.filepath, args.num_entries, args.mask_columns)

        # Train/test split
        df_train, df_test = train_test_split(df, test_size=0.1, random_state=42) if args.disable_split else (df, df)

        # Case 1: Pretraining on a large dataset followed by training
        if args.filepath_pretrain_dataset:
            reduced_data, reconstructed_data = pretrain_and_train(args.filepath_pretrain_dataset, args.filepath_save_pretrain, df_train, df_test)

        # Case 2: Refinement using a pre-trained model
        elif args.filepath_pretrained_model:
            reduced_data, reconstructed_data = train_with_pretrained_model(args.filepath_pretrained_model, df_train, df_test)

        # Case 3: Standard training
        else:
            reduced_data, reconstructed_data = train_from_scratch(df_train, df_test)

        # Interpolator optimisation
        optimize_interpolator(reconstructed_data, reduced_data, 'Interpolator')

    except Exception as e:
        log_progress.error("Error in main: %s", e)
        

if __name__ == "__main__":
    main()
