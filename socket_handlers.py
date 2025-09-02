import numpy as np
from flask import current_app
from flask_socketio import emit
from logger import setup_logger

log = setup_logger("SocketHandlers")

def cursor_move(payload):
    """
    Socket.IO handler for 'cursor_move' events coming from the browser.
    Expects: {'u': [...], 'origin': 'keyboard'|'mouse'|'osc', 'seq': int}
    """
    try:
        u = payload.get("u")
        origin = payload.get("origin", None)
        seq = payload.get("seq", None)  # <— NEW
        if u is None:
            return

        u = np.asarray(u, dtype=float).ravel().tolist()

        interpolator = current_app.config["INTERPOLATOR"]
        osc_client   = current_app.config["OSC_CLIENT"]

        # 1) ricostruzione per UI
        y = interpolator.interpolate(u).flatten().tolist()

        # 2) echo verso UI (include 'seq' per dedup client-side)
        emit("cursor_update", {"u": u, "origin": origin, "y": y, "seq": seq})  # <— seq

        # 3) OSC best-effort
        try:
            interpolator.send_data(osc_client, u)
        except OSError as e:
            log.warning("OSC send failed (non-blocking): %s", e)

    except Exception as exc:
        log.error("cursor_move handler error: %s", str(exc))

