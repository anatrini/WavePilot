import ast
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import torch
from torch import nn

from logger import setup_logger

logging = setup_logger("Utils Logger")


# Set GPU device if available according to OS
def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


device = get_device()
print(f"Using device: {device}")


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
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            # Extract the best hyperparameters for the VAE
            if "Best VAE Parameters" in line:
                try:
                    params_str = line.split("Best VAE Parameters: ")[1].split(" |")[0]
                    params["vae"] = ast.literal_eval(params_str)
                except (IndexError, SyntaxError, ValueError) as e:
                    raise ValueError(f"Error processing VAE parameters from line: {line}. Details: {e}") from e

            # Extract the best hyperparameters for the interpolator
            elif "Best RBF Parameters" in line:
                try:
                    params_str = line.split("Best RBF Parameters: ")[1].split(" |")[0]
                    params["rbf"] = ast.literal_eval(params_str)
                except (IndexError, SyntaxError, ValueError) as e:
                    raise ValueError(f"Error processing interpolator parameters from line: {line}. Details: {e}") from e

    except FileNotFoundError as e:
        raise FileNotFoundError(f"The specified log file does not exist: {log_file}. Details: {e}") from e
    except IOError as e:
        raise IOError(f"Error reading the log file: {log_file}. Details: {e}") from e

    if not params:
        raise ValueError("No parameters found in the log file.")

    return params


# Get activation function module from string
def get_activation_function(activation_name):
    activation_functions = {
        "ReLU": nn.ReLU(),
        "LeakyReLU": nn.LeakyReLU(),
        "Sigmoid": nn.Sigmoid(),
        "ELU": nn.ELU(),
        "GELU": nn.GELU(),
    }
    return activation_functions.get(activation_name, None)


def select_random_entries(input_csv, ouput_csv, n):
    df = pd.read_csv(input_csv)
    df["ID"] = range(1, len(df) + 1)
    df.to_csv(input_csv, index=False)

    df_sample = df.sample(n)
    df_sample.to_csv(ouput_csv, index=False)


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


def plot_reconstruction_error(original_data, reduced_data, reconstructed_data):
    reconstruction_error = np.mean(np.square(original_data - reconstructed_data), axis=1)
    average_error = np.mean(reconstruction_error)
    print(average_error)

    # Get x, y, z cohordinates from reduced data
    x, y, z = reduced_data.T

    # Crea un grafico a dispersione 3D dell'errore di ricostruzione
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x, y=y, z=z, mode="markers", marker=dict(size=5, color=reconstruction_error, colorscale="Viridis")
            )
        ]
    )

    fig.update_layout(
        title="3D Scatter Plot of Reconstruction Error",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Reconstruction Error"),
    )
    fig.show()
