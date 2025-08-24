# serialization.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch

from model import DeterministicVAE
from utils import LatentScaler

from constants import CHECKPOINTS_FOLDER, CHECKPOINT_EXTENSION

CHECKPOINT_VERSION = "2.0"  # bump this if the checkpoint structure changes


def _assert_key(d: Dict[str, Any], key: str):
    if key not in d:
        raise ValueError(f"Checkpoint missing required key: '{key}'")


def save_model(
    reducer,                                # trained VectorReducer (or at least with a built model)
    vae_params: Dict[str, Any],             # best VAE parameters
    rbf_params: Optional[Dict[str, Any]],   # best RBF parameters
    filepath: str,
    *,
    latent_scaler: Optional[LatentScaler] = None,   # fitted scaler for latent space
    rbf_interpolator: Optional[Any] = None,         # fitted RBFInterpolator (optional)
    Z_std: Optional[np.ndarray] = None,             # normalised latent space used for RBF fitting (optional)
    original_data: Optional[np.ndarray] = None,     # target data used for RBF (optional, useful for refit)
    median_dist: Optional[float] = None             # median pairwise distance in latent space (optional)
) -> None:
    """
    Save a full checkpoint, including:
      - DeterministicVAE metadata and weights
      - best VAE and RBF parameters
      - optional latent scaler, RBF interpolator, and reference data

    Notes:
    - torch.save uses pickle: it can serialise SciPy objects if they are picklable.
    - If you do not wish to serialise the interpolator, pass rbf_interpolator=None
      and keep only the metadata.
    """
    if not hasattr(reducer, "model") or reducer.model is None:
        raise ValueError("Reducer has no trained model to save.")

    model: DeterministicVAE = reducer.model
    if not isinstance(model, DeterministicVAE):
        raise TypeError("Reducer.model is not a DeterministicVAE instance.")

    # Retrieve essential metadata to rebuild the model identically
    input_dim = int(reducer.num_features)
    latent_dim = int(reducer.latent_dim)
    kl_beta = float(model.kl_beta)
    deterministic = bool(model.deterministic)

    # Extract the exact hidden_dims from the trained encoder
    hidden_dims_used = []
    for layer in model.encoder_backbone:
        if isinstance(layer, torch.nn.Linear):
            hidden_dims_used.append(layer.out_features)

    checkpoint: Dict[str, Any] = {
        "version": CHECKPOINT_VERSION,
        "params": {
            "vae": vae_params or {},
            "rbf": rbf_params or {}
        },
        "model_meta": {
            "class": "DeterministicVAE",
            "input_dim": input_dim,
            "latent_dim": latent_dim,
            "hidden_dims": hidden_dims_used,
            "kl_beta": kl_beta,
            "deterministic": deterministic,
            "activation": "SiLU",  # for documentation: activation is fixed
        },
        "state_dict": model.state_dict(),
        "rbf_bundle": {
            "has_interpolator": rbf_interpolator is not None,
            "median_dist": float(median_dist) if median_dist is not None else None,
            "Z_std": Z_std if Z_std is not None else None,
            "original_data": original_data if original_data is not None else None,
            "interpolator": rbf_interpolator if rbf_interpolator is not None else None,
            "scaler": {
                "mu": getattr(latent_scaler, "mu", None),
                "sigma": getattr(latent_scaler, "sigma", None),
                "eps": getattr(latent_scaler, "eps", 1e-12),
            } if latent_scaler is not None else None,
        },
    }

    out_path = Path(filepath)
    if out_path.suffix == "":
        out_path = out_path.with_suffix(CHECKPOINT_EXTENSION)
    if out_path.parent == Path("") or str(out_path.parent) == ".":
        out_path = Path(CHECKPOINTS_FOLDER) / out_path.name

    out_path.parent.mkdir(parents=True, exist_ok=True)

    torch.save(checkpoint, str(out_path))


def load_model(
    filepath: str,
    map_location: Optional[torch.device] = None
) -> Tuple[DeterministicVAE, Dict[str, Any], Dict[str, Any]]:
    """
    Load a DeterministicVAE with its weights and metadata, and return
    the stored best parameters for both VAE and RBF.

    Returns:
        model       : DeterministicVAE set to eval()
        vae_params  : dict with best VAE parameters
        rbf_package : dict containing:
                        - "params": best RBF parameters
                        - "bundle": { "scaler": {...}, "median_dist": ..., "Z_std": ..., "original_data": ...,
                                      "has_interpolator": bool, "interpolator": obj|None }
    """
    ckpt = torch.load(filepath, map_location=map_location or torch.device("cpu"))

    # Basic integrity checks
    _assert_key(ckpt, "version")
    _assert_key(ckpt, "params")
    _assert_key(ckpt, "state_dict")
    _assert_key(ckpt, "model_meta")

    if ckpt["model_meta"].get("class") != "DeterministicVAE":
        raise ValueError("Unsupported model class in checkpoint (expected DeterministicVAE).")

    model_meta = ckpt["model_meta"]
    input_dim = int(model_meta["input_dim"])
    latent_dim = int(model_meta["latent_dim"])
    hidden_dims = list(model_meta["hidden_dims"])
    kl_beta = float(model_meta["kl_beta"])
    deterministic = bool(model_meta["deterministic"])

    # Rebuild the model exactly as it was saved
    model = DeterministicVAE(
        input_dim=input_dim,
        latent_dim=latent_dim,
        hidden_dims=hidden_dims,
        kl_beta=kl_beta,
        deterministic=deterministic,
        input_noise_std=0.0
    )
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    # Retrieve saved parameters
    vae_params = ckpt["params"].get("vae", {})
    rbf_params = ckpt["params"].get("rbf", {})

    # RBF package: scaler and optional interpolator
    rbf_bundle = ckpt.get("rbf_bundle", {})
    rbf_package = {
        "params": rbf_params,
        "bundle": rbf_bundle
    }

    return model, vae_params, rbf_package