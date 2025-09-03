import numpy as np

from flask import current_app
from flask_socketio import emit

from logger import setup_logger

log = setup_logger("SocketHandlers")

# aggiungi in cima al file se manca

def cursor_move(payload):
    """
    Expects: {'u': [...], 'seq': int}
    Emits back: {'u': [...], 'y': [...], 'seq': int}
    """
    try:
        u   = payload.get("u")
        seq = payload.get("seq", None)

        if u is None:
            return

        # normalizza formato
        u = np.asarray(u, dtype=float).ravel().tolist()

        interpolator = current_app.config["INTERPOLATOR"]
        osc_client   = current_app.config["OSC_CLIENT"]

        # 1) calcola la ricostruzione da inviare anche al client
        y = interpolator.interpolate(u)    # -> np.ndarray shape (1, D)
        y = np.asarray(y, dtype=float).ravel().tolist()

        # 2) invia comunque ai consumer audio/OSC (se ti serve mantenerlo)
        interpolator.send_data(osc_client, u)

        # 3) echo al browser: includi sia 'y' che 'seq'
        emit("cursor_update", {"u": u, "y": y, "seq": seq})

    except Exception as exc:
        log.error("cursor_move handler error: %s", str(exc))