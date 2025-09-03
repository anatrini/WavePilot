import numpy as np
import numpy as np
from flask import current_app, jsonify, render_template

def index_route():
    """Return the main HTML page."""
    return render_template("index.html")

def data_route():
    """
    Return latent data and metadata for the frontend.

    Reads:
      - LATENT_DATA: numpy-like (N, D) with values in [0,1]
      - PRESET_NAMES: optional list[str] length N (fallback to ID1..N)
    """
    latent_data = current_app.config.get("LATENT_DATA", None)
    if latent_data is None:
        # Defensive fallback
        return jsonify({
            "latent": [],
            "dim": 0,
            "bounds_min": [],
            "bounds_max": [],
            "preset_names": []
        })

    Z = np.asarray(latent_data, dtype=float)
    N = int(Z.shape[0]) if Z.ndim == 2 else 0
    D = int(Z.shape[1]) if Z.ndim == 2 else 0

    # Bounds in data-space [0,1] (used only for denormalization logic)
    bounds_min = Z.min(axis=0).tolist() if Z.size else []
    bounds_max = Z.max(axis=0).tolist() if Z.size else []

    # Preset names from app config or fallback to ID1..N
    preset_names = current_app.config.get("PRESET_NAMES")
    if not isinstance(preset_names, list) or len(preset_names) != N:
        preset_names = [f"ID{i+1}" for i in range(N)]

    return jsonify({
        "latent": Z.tolist(),
        "dim": D,
        "bounds_min": bounds_min,
        "bounds_max": bounds_max,
        "preset_names": preset_names
    })

