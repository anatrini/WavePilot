import ast
import hashlib
import json
import os
import random
import re
from typing import Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import torch

from logger import setup_logger

logging = setup_logger("Utils Logger")

# ----------------------- Tensor utilities ----------------------- #
def to_tensor(x: Union[np.ndarray, torch.Tensor], device: torch.device) -> torch.Tensor:
    """Convert to torch.FloatTensor on the specified device."""
    if isinstance(x, np.ndarray):
        return torch.from_numpy(x.astype(np.float32)).to(device)
    return x.to(device).float()


# ----------------------- Architecture helpers ----------------------- #
def round_to_multiple(n: int, base: int) -> int:
    """Round n to the nearest multiple of 'base' (>= base)."""
    if base <= 1:
        return n
    return max(base, int(round(n / base) * base))

def compute_hidden_dims(
    input_dim: int,
    latent_dim: int,
    width_scale: float = 1.0,  # >0
    depth: int = 2,            # {1,2,3}
    round_to: int = 8,         # multiple for stability
    min_hidden: int = 32,
    max_hidden: int = 2048
) -> list[int]:
    """
    Compute funnel-shaped hidden layers for MLP encoder/decoder based on input and latent dimensions.

    Parameters:
        depth: controls number of hidden layers
        width_scale: controls global capacity
    """
    depth = int(max(1, min(3, depth)))

    base_h1 = max(input_dim, 64)
    base_h2 = max(int(0.25 * (input_dim + 8 * latent_dim)), 32)
    base_h3 = max(int(0.5 * (base_h2 + 4 * latent_dim)), 32)

    def clamp_round(v: float) -> int:
        v = int(v * width_scale)
        v = max(min_hidden, min(max_hidden, v))
        return round_to_multiple(v, round_to)

    h1 = clamp_round(base_h1)
    h2 = clamp_round(base_h2)
    h3 = clamp_round(base_h3)

    if depth == 1:
        return [h1]
    elif depth == 2:
        return [h1, h2]
    else:
        # Enforce decreasing monotonicity to avoid expansion
        h2 = min(h2, h1)
        h3 = min(h3, h2)
        return [h1, h2, h3]
    


class LatentScaler:
    """
    Z-score scaler for latent coordinates:
    - fit(): stores per-dimension mean (mu) and std (sigma)
    - transform(): (Z - mu) / sigma with safe epsilon on sigma
    - inverse_transform(): Z' * sigma + mu
    """
    def __init__(self, eps: float=1e-12):
        self.mu = None
        self.sigma = None
        self.eps = float(eps)

    def fit(self, Z: np.ndarray):
        Z = np.asarray(Z, dtype=np.float64)
        self.mu = Z.mean(axis=0, keepdims=True)
        sigma = Z.std(axis=0, keepdims=True)
        self.sigma = np.where(sigma < self.eps, 1.0, sigma)
        return self

    def transform(self, Z: np.ndarray) -> np.ndarray:
        assert self.mu is not None and self.sigma is not None, "Call fit() first."
        Z = np.asarray(Z, dtype=np.float64)
        return (Z - self.mu) / self.sigma

    def inverse_transform(self, Zs: np.ndarray) -> np.ndarray:
        assert self.mu is not None and self.sigma is not None, "Call fit() first."
        Zs = np.asarray(Zs, dtype=np.float64)
        return Zs * self.sigma + self.mu


# ----------------------- Runtime & Reproducibility ----------------------- #
def get_device() -> torch.device:
    """Select GPU device if available according to OS."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")



def set_global_seeds(seed):
    """Set all random seeds to ensure reproducibility across runs."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    os.environ['PYTHONHASHSEED'] = str(seed)

    torch.use_deterministic_algorithms(True)


# ----------------------- File I/O & Parsing ----------------------- #
def load_osc_addresses(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            addresses = json.load(f)
        logging.info(f"Loaded {len(addresses)} OSC addresses from {file_path}")
        return addresses
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error loading OSC addresses: {e}")
    return []


def get_hyperparams_from_log(log_file):
    params = {}
    pat_vae = re.compile(r"Best VAE Parameters:\s*(\{.*\})")
    pat_rbf = re.compile(
        r"Best RBF Parameters:\s*(\{.*\})"
        r"(?:\s*\|\s*Validation\s+(?:distance|error):\s*([+\-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+\-]?\d+)?))?"
    )

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                m = pat_vae.search(line)
                if m:
                    try:
                        params["vae"] = ast.literal_eval(m.group(1))
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Error parsing VAE params from line: {line}") from e
                    continue

                m = pat_rbf.search(line)
                if m:
                    try:
                        params["rbf"] = ast.literal_eval(m.group(1))
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Error parsing RBF params from line: {line}")
                    # Validation distance (optional)
                    if m.group(2) is not None:
                        try:
                            params["rbf_best_value"] = float(m.group(2))
                        except ValueError:
                            pass

    except FileNotFoundError as e:
        raise FileNotFoundError(f"The specified log file does not exist: {log_file}. Details: {e}") from e
    except IOError as e:
        raise IOError(f"Error reading the log file: {log_file}. Details: {e}") from e

    if "vae" not in params and "rbf" not in params:
        raise ValueError("No parameters found in the log file!")

    return params


def remove_duplicate_lines(file_path):
    """Removes duplicate lines from a log file while preserving order."""
    seen_lines = set()
    unique_lines = []

    with open(file_path, "r") as file:
        for line in file:
            if line not in seen_lines:
                seen_lines.add(line)
                unique_lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(unique_lines)


# ----------------------- Search space versioning ----------------------- #
def space_fingerprint(space: dict) -> str:
    """Generate a short hash fingerprint of the hyperparameter search space for identification."""
    payload = json.dumps(space, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8]


# ----------------------- Dataset helpers ----------------------- #
def select_random_entries(input_csv, ouput_csv, n):
    df = pd.read_csv(input_csv)
    df["ID"] = range(1, len(df) + 1)
    df.to_csv(input_csv, index=False)

    df_sample = df.sample(n)
    df_sample.to_csv(ouput_csv, index=False)


# ----------------------- Visualization ----------------------- #
def plot_reconstruction_error(original_data, reduced_data, reconstructed_data):
    reconstruction_error = np.mean(np.square(original_data - reconstructed_data), axis=1)
    average_error = np.mean(reconstruction_error)
    print(average_error)

    # Get x, y, z coordinates from reduced data
    x, y, z = reduced_data.T

    # Create a 3D scatter plot of reconstruction error
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=5, color=reconstruction_error, colorscale="Viridis"))])
    
    fig.update_layout(
        title="3D Scatter Plot of Reconstruction Error",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Reconstruction Error"),
    )
    fig.show()
