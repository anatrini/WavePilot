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
    parser.add_argument(
        "-f", "--filepath", dest="filepath", type=str, required=True, help="Dataset of the presets to be reduced."
    )

    parser.add_argument(
        "-n",
        "--num_entries",
        dest="num_entries",
        type=int,
        required=True,
        default=None,
        help="Number of random entries to select from the dataset.",
    )

    # Large dataset of presets to pretrain the model (Optional)
    parser.add_argument(
        "-F",
        "--filepath_pretrain",
        dest="filepath_pretrain",
        type=str,
        default=None,
        help="Large dataset to pretrain the model.",
    )

    # Filepath where to save the pretrained model, only necessary if -F is passed
    parser.add_argument("-s", "--filepath_save_pretrain", dest="filepath_save_pretrain", type=str, default=None)

    parser.add_argument(
        "-d",
        "--disable_split",
        dest="disable_split",
        action="store_false",
        help="Disable train/test split and use the entire dataset for both training and validation. Default split enabled.",
    )

    return parser.parse_args()


log_progress: Logger = setup_logger("ProgressLogger", file=False)


# Load data
def load_data(filepath, num_entries=None):
    loader = DataLoader(filepath)
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
            if msg == "DONE":
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
            pretrained_model,
        )

        # Train the model
        reducer.train_vae(n_epochs)

        # Validate the model
        validation_error = compute_validation_error(reducer, original_test)

        # Move the model to cpu
        reducer.move_to_cpu()

        return validation_error, params, reducer.model

    except Exception as e:
        log_progress.error("Error during VAE optimization: %s", e)
        return float("inf"), params, None  # Ritorna un valore alto per continuare l'ottimizzazione
    finally:
        queue.put(1)  # Notify progress


def interpolate_and_validate(progress_queue, params, original_data, reduced_data, min_degree, fixed_epsilon_kernels):
    try:
        # Unpack parameters
        smoothing, kernel, epsilon, degree = params

        # Skip epsilon for certain kernels
        if kernel in fixed_epsilon_kernels:
            epsilon = 1.0

        # Ensure degree meets minimum requirements for certain kernels
        if kernel in min_degree and degree < min_degree[kernel]:
            log_progress.warning(
                "Skipping configuration: kernel=%s, degree=%d (below minimum degree requirement)", kernel, degree
            )
            progress_queue.put(1)
            return float("inf"), params  # Invalid configuration

        # Calculate the number of polynomial terms for the given degree
        num_poly_terms = 0 if degree == -1 else (degree + 1) * (degree + 2) // 2
        if original_data.shape[0] < num_poly_terms:
            log_progress.warning(
                "Skipping configuration: insufficient dataset size for degree=%d (requires %d entries)",
                degree,
                num_poly_terms,
            )
            progress_queue.put(1)
            return float("inf"), params

        interpolator = RBFInterpolator(
            reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon, degree=degree
        )

        # Validate interpolator
        interpolated_data = interpolator(reduced_data)
        distances = [
            euclidean(original, interpolated) for original, interpolated in zip(original_data, interpolated_data)
        ]
        validation_distance = np.mean(distances)

        # Log progress
        log_progress.info(
            "Configuration validated: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f, validation_distance=%.5f",
            kernel,
            degree,
            smoothing,
            epsilon,
            validation_distance,
        )
        progress_queue.put(1)

        return validation_distance, params

    except np.linalg.LinAlgError:
        # Handle singular matrix error
        log_progress.warning(
            "Skipping configuration due to singular matrix error: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f",
            kernel,
            degree,
            smoothing,
            epsilon,
        )
        progress_queue.put(1)
        return float("inf"), params

    except ValueError as e:
        # Handle specific ValueError for minimum data points
        if "At least" in str(e):
            log_progress.warning(
                "Skipping configuration due to insufficient data points: kernel=%s, degree=%d, smoothing=%.5f, epsilon=%.5f",
                kernel,
                degree,
                smoothing,
                epsilon,
            )
            progress_queue.put(1)
            return float("inf"), params
        else:
            raise e

    except Exception as e:
        # Handle any other exceptions
        log_progress.error("Unexpected error in interpolate_and_validate: %s", e)
        progress_queue.put(1)
        return float("inf"), params


def optimize_vae(df_train, df_test, log_prefix, save_pretrained_model=False, save_filepath=None, pretrained_model=None):

    # VAE's params' grid
    vae_grid = {
        "n_epochs": [50, 100, 200],
        "learning_rate": np.logspace(-6, -2, num=5),
        "weight_decay": np.logspace(-6, -2, num=5),
        "n_layers": list(range(1, 4)),
        "layer_dim": [64, 128, 256],
        "activation": ["ReLU", "LeakyReLU", "ELU", "GELU"],
        "kl_beta": np.linspace(0.01, 1.0, num=5),
        "mse_beta": np.linspace(0.1, 2.0, num=5),
    }

    # Get all combinations of hyperparameters
    param_combinations = list(itertools.product(*vae_grid.values()))
    total_combinations = len(param_combinations)

    # Logger configurations
    manager = Manager()
    progress_queue = manager.Queue()
    log_queue = manager.Queue()

    log = setup_logger("OptimizationLogger", log_queue=log_queue, file=True)
    listener_log = log_listener(log_queue, log.handlers)

    # Progress listener
    listener_process = Process(target=progress_listener, args=(progress_queue, total_combinations))
    listener_process.start()

    try:
        log_progress.info("%s Starting VAE optimization...", log_prefix)

        input_data = [
            (progress_queue, params[0], params[1:], df_train, df_test, pretrained_model)
            for params in param_combinations
        ]

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(train_and_validate, input_data)

        # Find the best result
        best_validation_error = float("inf")
        best_params = None
        best_model = None

        for idx, result in enumerate(results):
            validation_error, params, model = result

            n_epochs = input_data[idx][1]

            # Converti params in formato dizionario
            param_dict = {
                "num_epochs": n_epochs,
                "learning_rate": params[0],
                "weight_decay": params[1],
                "n_layers": params[2],
                "layer_dim": params[3],
                "activation_function": params[4],
                "kl_beta": params[5],
                "mse_beta": params[6],
            }

            log_progress.info("%s Validation Error: %.5f | Params: %s", log_prefix, validation_error, params)

            if validation_error < best_validation_error:
                best_validation_error = validation_error
                best_params = param_dict
                best_model = model

    except Exception as e:
        log_progress.error("%s Error during optimization: %s", log_prefix, e)
        raise

    finally:
        progress_queue.put("DONE")
        listener_process.join()
        log_queue.put(None)
        listener_log.stop()

    log.info("Best VAE hyperparams: %s with a validation error of %.5f", best_params, best_validation_error)

    if save_pretrained_model:
        torch.save(best_model, f"{save_filepath}.pt")

    return best_params, best_model


def optimize_interpolator(original_data, reduced_data, log_prefix):
    # Interpolator's params' grid
    interpolator_grid = {
        "smoothing": np.linspace(0.0, 1.0, num=50),
        "kernel": [
            "multiquadric",
            "inverse_multiquadric",
            "inverse_quadratic",
            "gaussian",
            "linear",
            "quintic",
            "cubic",
            "thin_plate_spline",
        ],
        "epsilon": np.linspace(1e-03, 3.0, num=30),
        "degree": np.linspace(-1, 2, num=4, dtype=int),
    }

    # Minimum degree requirements for each kernel
    min_degree = {"multiquadric": 0, "linear": 0, "thin_plate_spline": 1, "cubic": 1, "quintic": 2}

    # Kernels for which epsilon should be set to 1
    fixed_epsilon_kernels = ["linear", "thin_plate_spline", "cubic", "quintic"]

    param_combinations = list(itertools.product(*interpolator_grid.values()))
    total_combinations = len(param_combinations)

    # Configura logger
    manager = Manager()
    progress_queue = manager.Queue()
    log_queue = manager.Queue()

    log = setup_logger("OptimizationLogger", log_queue=log_queue, file=True)
    listener_log = log_listener(log_queue, log.handlers)

    # Listener per il progresso
    listener_process = Process(target=progress_listener, args=(progress_queue, total_combinations))
    listener_process.start()

    try:
        log_progress.info("%s Starting interpolator optimization with %d combinations", log_prefix, total_combinations)

        input_data = [
            (progress_queue, params, original_data, reduced_data, min_degree, fixed_epsilon_kernels)
            for params in param_combinations
        ]

        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(interpolate_and_validate, input_data)

        # Find the best result
        best_validation_distance = float("inf")
        best_params = None

        for validation_distance, params in results:
            param_dict = {"smoothing": params[0], "kernel": params[1], "epsilon": params[2], "degree": params[3]}

            log_progress.info("%s Validation Distance: %.5f | Params: %s", log_prefix, validation_distance, param_dict)

            if validation_distance < best_validation_distance:
                best_validation_distance = validation_distance
                best_params = param_dict

    except Exception as e:
        log_progress.error("%s Error during interpolator optimization: %s", log_prefix, e)
        raise

    finally:
        progress_queue.put("DONE")
        listener_process.join()
        log_queue.put(None)
        listener_log.stop()

    log.info(
        "%s Best Interpolator params: %s with a validation distance of %.5f",
        log_prefix,
        best_params,
        best_validation_distance,
    )

    return best_params


def main():

    try:
        args = get_arguments()
        torch.manual_seed(42)

        filepath = args.filepath
        num_entries = args.num_entries
        filepath_pretrain = args.filepath_pretrain
        filepath_save_pretrain = args.filepath_save_pretrain
        disable_split = args.disable_split

        df = load_data(filepath, num_entries)

        if disable_split:
            df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
        else:
            df_train, df_test = df, df

        if filepath_pretrain:
            df_pretrain = load_data(filepath_pretrain)
            df_train_pretrain, df_test_pretrain = train_test_split(df_pretrain, test_size=0.2, random_state=42)
            best_params_pretrain, best_model_pretrain = optimize_vae(
                df_train_pretrain,
                df_test_pretrain,
                "Pretrain",
                save_pretrained_model=True,
                save_filepath=filepath_save_pretrain,
            )
            best_params_train, _ = optimize_vae(df_train, df_test, "Train", pretrained_model=best_model_pretrain)

            (
                n_epochs_pretrain,
                learning_rate_pretrain,
                weight_decay_pretrain,
                n_layers_pretrain,
                layer_dim_pretrain,
                activation_name_pretrain,
                kl_beta_pretrain,
                mse_beta_pretrain,
            ) = best_params_pretrain
            activation_pretrain = get_activation_function(activation_name_pretrain)
            reducer_pretrain = VectorReducer(
                df_pretrain,
                learning_rate_pretrain,
                weight_decay_pretrain,
                n_layers_pretrain,
                layer_dim_pretrain,
                activation_pretrain,
                kl_beta_pretrain,
                mse_beta_pretrain,
            )
            reducer_pretrain.train_vae(n_epochs_pretrain)

            (
                n_epochs_train,
                learning_rate_train,
                weight_decay_train,
                n_layers_train,
                layer_dim_train,
                activation_name_train,
                kl_beta_train,
                mse_beta_train,
            ) = best_params_train
            activation_train = get_activation_function(activation_name_train)
            pretrained_model = torch.load(f"{filepath_save_pretrain}.pt")
            reducer_train = VectorReducer(
                df,
                learning_rate_train,
                weight_decay_train,
                n_layers_train,
                layer_dim_train,
                activation_train,
                kl_beta_train,
                mse_beta_train,
                pretrained_model=pretrained_model,
            )
            reducer_train.train_vae(n_epochs_train)
            reduced_data, reconstructed_data = reducer_train.vae()

        else:
            best_params_train, _ = optimize_vae(df_train, df_test, "Train")

            n_epochs_train = best_params_train["num_epochs"]
            learning_rate_train = best_params_train["learning_rate"]
            weight_decay_train = best_params_train["weight_decay"]
            n_layers_train = best_params_train["n_layers"]
            layer_dim_train = best_params_train["layer_dim"]
            activation_name_train = best_params_train["activation_function"]
            kl_beta_train = best_params_train["kl_beta"]
            mse_beta_train = best_params_train["mse_beta"]

            activation_train = get_activation_function(activation_name_train)
            reducer_train = VectorReducer(
                df_train,
                learning_rate_train,
                weight_decay_train,
                n_layers_train,
                layer_dim_train,
                activation_train,
                kl_beta_train,
                mse_beta_train,
            )

            reducer_train.train_vae(n_epochs_train)

            reduced_data, reconstructed_data = reducer_train.vae()

            # print(f"Reduced data is on device: {reducer_train.device}")

        optimize_interpolator(reconstructed_data, reduced_data, "Interpolator")

    except Exception as e:
        log_progress.error("Error in main: %s", e)


if __name__ == "__main__":
    main()

# num_entries = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, n/2]
