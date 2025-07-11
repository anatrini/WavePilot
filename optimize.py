from multiprocessing import cpu_count

import numpy as np
import optuna
from optuna.samplers import TPESampler
from optuna.storages import RDBStorage

from scipy.interpolate import RBFInterpolator
from scipy.spatial.distance import mahalanobis
from tqdm import tqdm

from constants import (
    N_TRIALS_RBF,
    N_TRIALS_VAE,
    GLOBAL_SEED,
    RBF_FIXED_EPSILON_KERNELS,
    RBF_MIN_DEGREE,
    RBF_PARAM_RANGES,
    VAE_PARAM_RANGES,
)

from data import DataLoader
from dispatcher import SUGGEST_DISPATCH
from logger import setup_logger
from model import VectorReducer
from utils import get_activation_function, set_global_seeds




set_global_seeds(GLOBAL_SEED)

optuna.logging.set_verbosity(optuna.logging.WARNING)

log = setup_logger('OptimizationLogger', file=True)
log_progress = setup_logger('ProgressLogger', file=False)


# Load data
def load_data(filepath, num_entries=None, mask_columns=None):
    loader = DataLoader(filepath, mask_columns)
    df = loader.load_presets()

    if num_entries:
        #np.random.seed(ENTRY_SELECTION_RANDOM_SEED)
        selected_idx = np.random.choice(df.shape[0], size=num_entries, replace=False)
        df = df[selected_idx]

        log_progress.info("Randomly selected %d entries from the dataset", num_entries)
        log_progress.info("Selected indices from dataset: %s", selected_idx)
    else:
        log_progress.info("Using the entire dataset!")

    return df


def train_and_validate(n_epochs, params, original_df):
    try:
        learning_rate = params['learning_rate']
        weight_decay = params['weight_decay']
        n_layers = params['n_layers']
        layer_dim = params['layer_dim']
        activation_name = params['activation_function']
        kl_beta = params['kl_beta']
        recon_alpha = params['recon_alpha']
        dropout_rate = params['dropout_rate']
        latent_dim = params['latent_dim']
        kl_threshold = params['kl_threshold']
        annealing_epochs = params['annealing_epochs']

        activation = get_activation_function(activation_name)

        reducer = VectorReducer(
            original_df,
            learning_rate,
            weight_decay,
            n_layers,
            layer_dim,
            activation,
            kl_beta,
            recon_alpha,
            dropout_rate,
            latent_dim,
            kl_threshold,
            annealing_epochs
        )

        reducer.train_vae(n_epochs)
        validation_error = reducer.compute_loss(original_df, epoch=0, compute_gradients=False)
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

        cov_matrix = np.cov(original_data, rowvar=False)
        try:
            inv_cov = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            try:
                inv_cov = np.linalg.pinv(cov_matrix)
            except Exception as e:
                log_progress.warning("Fallback to identity matrix: %s", str(e))
                inv_cov = np.eye(original_data.shape[1])

        # Estimate distance with fallback
        distances = []
        for i in range(len(original_data)):
            try:
                d = mahalanobis(original_data[i], interpolated_data[i], inv_cov)
            except Exception as e:
                log_progress.warning("Mahalanobis failed, using Euclidean: %s", str(e))
                d = np.linalg.norm(original_data[i] - interpolated_data[i])
            distances.append(d)

        # Add penalty for out of range values
        out_of_bounds = np.sum((interpolated_data < 0) | (interpolated_data > 1))
        penalty = out_of_bounds / interpolated_data.size
        mean_distance = np.mean(distances)
        validation_distance = mean_distance + 30 * (penalty ** 1.5)

        #log_progress.info(f"Config: kernel={kernel}, smoothing={smoothing}, epsilon={epsilon}")
        #log_progress.info(f"Mean distance: {mean_distance:.4f}, Penalty: {penalty:.4f}, Total: {validation_distance:.4f}")

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
    # Since dataset are meant to be fairly small (< 150 samples)
    # There's no train test split
    # Model performance are evaluated on the entire dataset
    def __init__(self, df):
        self.df = df
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
            self.df
        )

        return validation_error


    def optimize_vae(self, n_trials=N_TRIALS_VAE):
        # Config a reproducible sampler
        sampler = TPESampler(
            seed=GLOBAL_SEED,
            n_startup_trials=10,
            consider_prior=True,
            prior_weight=1.0
        )

        # Set storage
        storage = RDBStorage(
            url="sqlite:///wavepilot_vae.db",
            engine_kwargs={"connect_args": {"timeout": 30}}
            )

        self.study_vae = optuna.create_study(
            direction="minimize",
            sampler=sampler,
            storage=storage,
            study_name="wavepilot_vae_study",
            load_if_exists=True
            )

        # Setup progress callback
        pbar = TQDMProgressBar(n_trials)

        # Execute optimization
        self.study_vae.optimize(
            self.objective_vae, 
            n_trials=n_trials, 
            n_jobs=cpu_count(), 
            callbacks=[pbar],
            show_progress_bar=True)

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

        sampler = TPESampler(
            seed=GLOBAL_SEED,
            n_startup_trials=5,
            consider_prior=True,
            prior_weight=1.0
        )

        storage = RDBStorage(
            url="sqlite:///wavepilot_rbf.db",
            engine_kwargs={"connect_args": {"timeout": 30}}
        )

        self.study_rbf = optuna.create_study(
            direction="minimize", 
            sampler=sampler,
            storage=storage,
            study_name="wavepilot_rbf_study",
            load_if_exists=True
            )

        pbar = TQDMProgressBar(n_trials)

        self.study_rbf.optimize(
            lambda trial: self.objective_rbf(trial, original_data, reduced_data),
            n_trials=n_trials,
            n_jobs=cpu_count(),
            callbacks=[pbar],
            show_progress_bar=True
            )

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
        best_params_train["recon_alpha"],
        best_params_train["dropout_rate"],
        best_params_train["latent_dim"],
        best_params_train["kl_threshold"],
        best_params_train["annealing_epochs"]
    )

    reducer_train.train_vae(best_params_train["num_epochs"])
    return reducer_train.vae()


def main(filepath, num_entries, mask_columns):

    df = load_data(filepath, num_entries, mask_columns)

    optimizer = Optimizer(df)

    best_vae_params = optimizer.optimize_vae()
    reduced_data, reconstructed_data = run_training(best_vae_params, df)

    best_rbf_params = optimizer.optimize_rbf(reduced_data, reconstructed_data)

    log_progress.info("Best VAE Parameters: %s", best_vae_params)
    log_progress.info("Best RBF Parameters: %s", best_rbf_params)

    log.info("Best VAE Parameters: %s | Validation error: %.10f", best_vae_params, optimizer.study_vae.best_value)
    log.info("Best RBF Parameters: %s | Validation distance: %.10f", best_rbf_params, optimizer.study_rbf.best_value)
