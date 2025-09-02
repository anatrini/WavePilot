import numpy as np
from flask import current_app, jsonify, render_template

def index_route():
    # Returns the HTML
    return render_template("index.html")

def data_route():
    # Read latent data from app config (set in run flask)
    latent_data = current_app.config["LATENT_DATA"]
    Z = np.asarray(latent_data, dtype=float)
    bounds_min = Z.min(axis=0).tolist() if Z.size else []
    bounds_max = Z.max(axis=0).tolist() if Z.size else []
    return jsonify({
        "latent": Z.tolist(),
        "dim": int(Z.shape[1]) if Z.ndim == 2 else 0,
        "bounds_min": bounds_min,
        "bounds_max": bounds_max
    })
