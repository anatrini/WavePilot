import argparse
import optuna
from multiprocessing import cpu_count

import numpy as np
from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from constants import OPTUNA_RANDOM_SEED, ENTRY_SELECTION_RANDOM_SEED, TRAIN_TEST_SPLIT_RANDOM_SEED, VAE_PARAM_RANGES, RBF_PARAM_RANGES, RBF_MIN_DEGREE, RBF_FIXED_EPSILON_KERNELS, N_TRIALS_VAE, N_TRIALS_RBF
from data import DataLoader
from dispatcher import SUGGEST_DISPATCH
from logger import setup_logger
from model import VectorReducer
from utils import get_activation_function


optuna.logging.set_verbosity(optuna.logging.WARNING)

log = setup_logger('OptimizationLogger', file=True)
log_progress = setup_logger('ProgressLogger', file=False)


def get_arguments():
    parser = argparse.ArgumentParser()

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

    parser.add_argument('-d', '--disable_split',
                        dest='disable_split',
                        action='store_false',
                        help='Disable train/test split and use the entire dataset for both training and validation. Default split enabled.')
    
    parser.add_argument('-t', '--test_size',
                        dest='test_size',
                        type=float,
                        default=0.2,
                        help='Train test split size, only available if -d flag is not provided. Default size 0.2.')
    
    parser.add_argument('-m', '--mask_columns',
                        dest='mask_columns',
                        type=str,
                        nargs='+',  # Permette di passare una lista di stringhe
                        default=None,
                        help='List of parameter names to be masked (excluded) from the dataset.')

    return parser.parse_args()



# Load data
def load_data(filepath, num_entries=None, mask_columns=None):
    loader = DataLoader(filepath, mask_columns)
    df = loader.load_presets()

    if num_entries:
        np.random.seed(ENTRY_SELECTION_RANDOM_SEED)
        selected_idx = np.random.choice(df.shape[0], size=num_entries, replace=False)
        df = df[selected_idx]
        log_progress.info("Randomly selected %d entries from the dataset", num_entries)
        log_progress.info("Selected indices from dataset: %s", selected_idx)
    else:
        log_progress.info("Using the entire dataset!")

    return df


def train_and_validate(n_epochs, params, original_train, original_test, pretrained_model=None):
    try:
        learning_rate = params['learning_rate']
        weight_decay = params['weight_decay']
        n_layers = params['n_layers']
        layer_dim = params['layer_dim']
        activation_name = params['activation_function']
        kl_beta = params['kl_beta']
        mse_beta = params['mse_beta']

        activation = get_activation_function(activation_name)

        reducer = VectorReducer(
            original_train,
            learning_rate,
            weight_decay,
            n_layers,
            layer_dim,
            activation,
            kl_beta,
            mse_beta,
            pretrained_model
        )

        reducer.train_vae(n_epochs)
        validation_error = reducer.compute_loss(original_test, compute_gradients=False)
        reducer.move_to_cpu()

        return validation_error, params, reducer.model

    except Exception as e:
        log_progress.error("Error during VAE optimization: %s", e, exc_info=True)
        return float('inf'), params



def interpolate_and_validate(params, original_data, reduced_data, min_degree, fixed_epsilon_kernels):
    try:
        smoothing = params['smoothing']
        kernel = params['kernel']
        epsilon = params['epsilon']
        degree = params['degree']

        # Gestisci epsilon e degree secondo le regole precedenti
        if kernel in fixed_epsilon_kernels:
            epsilon = 1.0

        if kernel in min_degree and degree < min_degree[kernel]:
            log_progress.warning("Skipping configuration: kernel=%s, degree=%d below minimum requirement", kernel, degree)
            return float('inf'), params

        num_poly_terms = 0 if degree == -1 else (degree + 1) * (degree + 2) // 2
        if original_data.shape[0] < num_poly_terms:
            log_progress.warning("Skipping configuration: insufficient dataset size for degree=%d", degree)
            return float('inf'), params

        interpolator = RBFInterpolator(
            reduced_data,
            original_data,
            smoothing=smoothing,
            kernel=kernel,
            epsilon=epsilon,
            degree=degree
        )

        interpolated_data = interpolator(reduced_data)
        distances = [
            euclidean(original, interpolated)
            for original, interpolated in zip(original_data, interpolated_data)
        ]

        validation_distance = np.mean(distances)
        return validation_distance, params

    except np.linalg.LinAlgError:
        log_progress.warning("Singular matrix error with kernel=%s, degree=%d", kernel, degree)
        return float('inf'), params

    except ValueError as e:
        if "At least" in str(e):
            log_progress.warning("Insufficient data points: kernel=%s, degree=%d", kernel, degree)
            return float('inf'), params
        else:
            log_progress.error("Unexpected ValueError: %s", e, exc_info=True)
            raise e

    except Exception as e:
        log_progress.error("Unexpected error in interpolate_and_validate: %s", e, exc_info=True)
        return float('inf'), params
    

class TQDMProgressBar:
    def __init__(self, total_trials):
        self.pbar = tqdm(total=total_trials)
    
    def __call__(self, study, trial):
        self.pbar.update(1)


class Optimizer:
    def __init__(self, df_train, df_test):
        self.df_train = df_train
        self.df_test = df_test
        self.study_vae = None
        self.study_rbf = None

    def objective_vae(self, trial):
        """Objective function for VAE"""
        params = {
            name: SUGGEST_DISPATCH[config["type"]](trial, name, config)
            for name, config in VAE_PARAM_RANGES.items()
        }

        validation_error, _, _ = train_and_validate(
            params['num_epochs'],
            params,
            self.df_train,
            self.df_test
        )

        return validation_error


    def optimize_vae(self, n_trials=N_TRIALS_VAE):
        pbar = TQDMProgressBar(n_trials)
        self.study_vae = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=OPTUNA_RANDOM_SEED))
        self.study_vae.optimize(self.objective_vae, n_trials=n_trials, n_jobs=cpu_count(), callbacks=[pbar])

        best_params = self.study_vae.best_params
        return best_params


    def objective_rbf(self, trial, original_data, reduced_data):
        """Objective function for RBF"""
        params = {
            name: SUGGEST_DISPATCH[config["type"]](trial, name, config)
            for name, config in RBF_PARAM_RANGES.items()
        }

        validation_distance, _ = interpolate_and_validate(
            params,
            original_data,
            reduced_data,
            RBF_MIN_DEGREE,
            RBF_FIXED_EPSILON_KERNELS
        )

        return validation_distance

    def optimize_rbf(self, original_data, reduced_data, n_trials=N_TRIALS_RBF):
        pbar = TQDMProgressBar(n_trials)
        self.study_rbf = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=OPTUNA_RANDOM_SEED))
        self.study_rbf.optimize(
            lambda trial: self.objective_rbf(trial, original_data, reduced_data),
            n_trials=n_trials,
            n_jobs=cpu_count(),
            callbacks=[pbar])

        best_params = self.study_rbf.best_params
        return best_params



def run_training(best_params_train, df_train):
    """Executes training with the best parameters found."""
    reducer_train = VectorReducer(
        df_train,
        best_params_train["learning_rate"],
        best_params_train["weight_decay"],
        best_params_train["n_layers"],
        best_params_train["layer_dim"],
        get_activation_function(best_params_train["activation_function"]),
        best_params_train["kl_beta"],
        best_params_train["mse_beta"]
    )

    reducer_train.train_vae(best_params_train["num_epochs"])
    return reducer_train.vae()


def main():

    args = get_arguments()
    filepath = args.filepath
    num_entries = args.num_entries
    test_size = args.test_size
    mask_columns = args.mask_columns

    df = load_data(filepath, num_entries, mask_columns)
    df_train, df_test = train_test_split(df, test_size=test_size, random_state=TRAIN_TEST_SPLIT_RANDOM_SEED) if args.disable_split else (df, df)

    optimizer = Optimizer(df_train, df_test)

    best_vae_params = optimizer.optimize_vae()
    reduced_data, reconstructed_data = run_training(best_vae_params, df_train)

    best_rbf_params = optimizer.optimize_rbf(reduced_data, reconstructed_data)

    log_progress.info("Best VAE Parameters: %s", best_vae_params)
    log_progress.info("Best RBF Parameters: %s", best_rbf_params)

    log.info("Best VAE Parameters: %s | Validation error: %.10f", best_vae_params, optimizer.study_vae.best_value)
    log.info("Best RBF Parameters: %s | Validation distance: %.10f", best_rbf_params, optimizer.study_rbf.best_value)

if __name__ == "__main__":
    main()

