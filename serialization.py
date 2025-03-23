import torch
from model import VAE
from utils import get_activation_function


def save_model(model, input_dim, n_layers, layer_dim, activation_name, filepath):
    """
    Save a VAE model with architecture metadata and weights.

    Args:
        model (VAE): The trained VAE model.
        input_dim (int): Input dimension of the model.
        n_layers (int): Number of layers in the encoder/decoder.
        layer_dim (int): Size of each layer.
        activation_name (str): Activation function used ("GELU", "ReLU", etc.).
        filepath (str): Path to save the model.
    """
    checkpoint = {
        "input_dim": input_dim,
        "architecture": {
            "n_layers": n_layers,
            "layer_dim": layer_dim,
            "activation": activation_name
        },
        "state_dict": model.state_dict()
    }

    torch.save(checkpoint, filepath)


def load_model(filepath):
    """
    Load a saved VAE model from disk.

    Returns:
        model (VAE): The loaded model in eval mode.
        architecture (dict): The architecture metadata.
    """
    checkpoint = torch.load(filepath, map_location=torch.device("cpu"))

    # Extract architecture
    input_dim = checkpoint["input_dim"]
    arch = checkpoint["architecture"]
    activation = get_activation_function(arch["activation"])

    model = VAE(
        input_dim=input_dim,
        n_layers=arch["n_layers"],
        layer_dim=arch["layer_dim"],
        activation=activation
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    return model, arch
