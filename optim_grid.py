import argparse
import itertools

import numpy as np
import torch
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split
from vae_model import VectorReducer

from data import DataLoader
from logger import setup_logger
from utils import *


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


logging = setup_logger("Grid Opmization Session", file=True)


# Load data
def load_data(filepath, num_entries=None):
    loader = DataLoader(filepath)
    df = loader.load_presets()

    if num_entries:
        df = df.sample(n=num_entries, random_state=42)
        logging.info(f"Randomly selected {num_entries} entries from ther dataset.")
    else:
        logging.info(f"Using the entire dataset.")

    return df


# Compute KL divergence
def kl_divergence(mu, logvar):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())


# Calculate validation error
def compute_validation_error(model, data):
    data_tensor = torch.tensor(data.values).float()
    with torch.no_grad():
        return model.compute_loss(data_tensor, compute_gradients=False)


def optimize_vae(df_train, df_test, log_prefix, save_pretrained_model=False, save_filepath=None, pretrained_model=None):

    # VAE's params' grid
    vae_grid = {
        "n_epochs": [5, 10, 25, 50, 100, 150, 200],
        "learning_rate": np.logspace(-5, -2, num=10),
        "weight_decay": np.logspace(-5, -2, num=5),
        "n_layers": list(range(1, 7)),
        "activation": ["ReLU", "LeakyReLU", "Sigmoid", "Tanh"],
        "kl_beta": np.linspace(0.05, 0.5, num=20),
        "mse_beta": np.linspace(0.3, 1.0, num=20),
    }

    # Get all combinations of hyperparameters
    param_combinations = list(itertools.product(*vae_grid.values()))
    best_validation_error = float("inf")
    best_params = []
    best_model = None
    # best_reducer = None

    # Loop over all combinations of hyperparameters
    for i, params in enumerate(param_combinations):
        try:
            # unpack params
            n_epochs, learning_rate, weight_decay, n_layers, activation_name, kl_beta, mse_beta = params
            activation = get_activation_function(activation_name)

            # train the model
            reducer = VectorReducer(
                df_train, learning_rate, weight_decay, n_layers, activation, kl_beta, mse_beta, pretrained_model
            )
            reducer.train_vae(n_epochs)

            # compute validation error
            validation_error = compute_validation_error(reducer, df_test)
            print(f"{log_prefix} trial {i+1}/{len(param_combinations)}: validation_error = {validation_error}")

            # update best parameters if current model is better
            if validation_error < best_validation_error:
                best_validation_error = validation_error
                best_params = params
                best_model = reducer.model
                # best_reducer = reducer

        except Exception as e:
            logging.error(f"Error during VAE optimization: {e}")

    if save_pretrained_model:
        # Save the pretrained model
        torch.save(best_model, f"{save_filepath}.pt")

    else:
        # Save best VAE params and log the best hyperparameters and validation error
        logging.info(f"Best VAE hyperparams: {best_params} with a validation error of {best_validation_error}")

    return best_params, best_model  # , best_reducer


def optimize_interpolator(df, reducer, log_prefix):

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
        "degree": np.linspace(-1, 2, num=4),
    }

    # Minimum degree requirements for each kernel
    min_degree = {"multiquadric": 0, "linear": 0, "thin_plate_spline": 1, "cubic": 1, "quintic": 2}

    # Kernels for which epsilon should be set to 1
    fixed_epsilon_kernes = ["linear", "thin_plate_spline", "cubic", "quintic"]

    param_combinations = list(itertools.product(*interpolator_grid.values()))
    best_validation_distance = float("inf")
    # print(f'Best validation distance of: {best_validation_distance}')
    best_params = []

    # Get the number of rows in the dataset
    df_size = df.shape[0]
    count = 0

    # Loop over all combinations of hyperparameters
    for i, params in enumerate(param_combinations):
        try:
            # unpack params
            smoothing, kernel, epsilon, degree = params

            # Skip epsilon for certain kernels
            if kernel in fixed_epsilon_kernes:
                epsilon = 1.0

            # Ensure degree meets minimum requiriments for certain kernels
            if kernel in min_degree and degree < min_degree[kernel]:
                continue

            # Calculate the number of polynomial terms for the given degree
            num_poly_terms = 0 if degree == -1 else (degree + 1) * (degree + 2) // 2
            if df_size < num_poly_terms:
                print(
                    f"Insufficient dataset size for kernel={kernel}, epsilon={epsilon}, smoothing={smoothing}, degree={degree}, skipping this configuration..."
                )
                continue

            # train the model
            # original_data = df.drop(columns=['ID', 'name', 'file'])
            original_data = original_data.values
            reduced_data, _ = reducer.vae()
            reduced_data = reduced_data[:, 1:]

            # train the interpolator
            interpolator = RBFInterpolator(
                reduced_data, original_data, smoothing=smoothing, kernel=kernel, epsilon=epsilon, degree=degree
            )
            interpolated_data = interpolator(reduced_data)

            # Compute euclidean distance between original and reduced vectors
            distances = []
            for original, interpolated in zip(original_data, interpolated_data):
                distance = euclidean(original, interpolated)
                distances.append(distance)

            validation_distance = np.mean(distances)
            print(
                f"{log_prefix} trial {i+1}/{len(param_combinations)}: validation_distance = {validation_distance} and {best_validation_distance}"
            )

            if validation_distance < best_validation_distance:
                best_validation_distance = validation_distance
                best_params = params
                count += 1
                print(f"This is the best combinations of params no. {count} : {best_params}")

        # Handling specific exceptions within the function to ensure the computation continues
        except np.linalg.LinAlgError:
            # Handles the singular matrix error and continues with the next configuration
            print(
                f"Singular matrix encountered with kernel={kernel}, epsilon={epsilon}, smoothing={smoothing}, degree={degree}, skipping this configuration..."
            )
        except ValueError as e:
            # Handles the specific error that requires a minimum number of data points and continues with the next configuration
            if "At least" in str(e):
                print(
                    f"Error encountered with kernel={kernel}, epsilon={epsilon}, smoothing={smoothing}, degree={degree}: {e}, skipping this configuration..."
                )
            else:
                # Raises other ValueError exceptions that are not specifically handled
                raise e

    # Save best VAE params and log the best hyperparameters and validation error
    logging.info(f"Best RBF params: {best_params} with a validation error of {best_validation_distance}")


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
            # Optimize and train the VAE to find the best pretrain params
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
                activation_train,
                kl_beta_train,
                mse_beta_train,
                pretrained_model=pretrained_model,
            )
            reducer_train.train_vae(n_epochs_train)

        else:
            # Without transfer learning, the VAE optimisation occurs on df_train, from which best_train_params is obtained
            # This is then passed to a full training loop, so that the resulting reducer is computed on the entire dataset,
            # and the RBF optimization can be performed on the entire dataset
            best_params_train, _ = optimize_vae(df_train, df_test, "Train")

            (
                n_epochs_train,
                learning_rate_train,
                weight_decay_train,
                n_layers_train,
                activation_name_train,
                kl_beta_train,
                mse_beta_train,
            ) = best_params_train
            activation_train = get_activation_function(activation_name_train)
            reducer_train = VectorReducer(
                df,
                learning_rate_train,
                weight_decay_train,
                n_layers_train,
                activation_train,
                kl_beta_train,
                mse_beta_train,
            )
            reducer_train.train_vae(n_epochs_train)

        optimize_interpolator(df, reducer_train, "Interpolator")

    except Exception as e:
        logging.error(f"Error in main: {e}")


if __name__ == "__main__":
    main()
