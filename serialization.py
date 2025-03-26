import torch
from model import VAE
from utils import get_activation_function


def save_model(model, vae_params: dict, rbf_params: dict, filepath: str):

    checkpoint = {
        "params": {
            "vae": vae_params,
            "rbf": rbf_params
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

    if "params" not in checkpoint or "state_dict" not in checkpoint:
        raise ValueError("Checkpoint file is missing required keys.")

    params = checkpoint["params"]
    vae_params = params["vae"]
    rbf_params = params["rbf"]

    activation = get_activation_function(vae_params["activation_function"])
    model = VAE(
        input_dim=vae_params["input_dim"],
        n_layers=vae_params["n_layers"],
        layer_dim=vae_params["layer_dim"],
        activation=activation
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    return model, vae_params, rbf_params
