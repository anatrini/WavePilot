# socket_handlers.py
# British English comments. No nested functions.

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

import numpy as np
from flask import current_app
from flask_socketio import emit
from logger import setup_logger

log = setup_logger("SocketHandlers")

# ---------- Flood control (web → ReaLearn) ----------
MAX_HZ = 30.0     # cap towards ReaLearn
EPSILON = 1e-4    # ignore tiny moves

@dataclass
class _CursorGate:
    last_t: float = 0.0
    last_u: List[float] | None = None

    def allow(self, u: List[float]) -> bool:
        now = time.monotonic()
        if now - self.last_t < (1.0 / MAX_HZ):
            return False
        if self.last_u is not None and len(self.last_u) == len(u):
            if all(abs(a - b) < EPSILON for a, b in zip(self.last_u, u)):
                return False
        self.last_t = now
        self.last_u = u[:]
        return True

_gate = _CursorGate()


def _coerce_cursor(payload) -> List[float] | None:
    """Accept {'cursor': [...]} or legacy {'u': [...]}; return flat list of floats or None."""
    if not isinstance(payload, dict):
        return None
    raw = payload.get("cursor", payload.get("u"))
    if raw is None:
        return None
    try:
        return np.asarray(raw, dtype=float).ravel().tolist()
    except Exception:
        return None


def register_addr_list(payload):
    """
    Controller → web-app (one-off at startup)
    Payload: {"paths": ["/param1", "/param2", ...]}  (order matches y indexes)
    Stores list under app.config["OSC_ADDR_LIST"] and acknowledges.
    """
    try:
        paths = payload.get("paths") if isinstance(payload, dict) else None
        if not (isinstance(paths, list) and all(isinstance(p, str) for p in paths)):
            log.warning("addr_list payload invalid: %r", payload)
            return
        current_app.config["OSC_ADDR_LIST"] = paths
        emit("addr_list_ack", {"count": len(paths)})
        log.info("Registered %d OSC param addresses.", len(paths))
    except Exception as exc:
        log.debug("register_addr_list error: %s", exc)


def cursor_move(payload):
    """
    Browser/UI → server:
      Expected: {'cursor': [x, y, z, ...]}  (legacy {'u': [...]} accepted)

    Behaviour:
      • Interpolate y for UI feedback;
      • Throttle (30 Hz) + epsilon before egress;
      • Send ONE OSC message per parameter using app.config['OSC_ADDR_LIST'] via interpolator.send_data(...).
    """
    # ---- DO NOT return after this point unless strictly necessary,
    # ---- to avoid Pylint's 'unreachable code' false positives.

    u = _coerce_cursor(payload)
    if u is None:
        return

    # Get dependencies from app config
    interpolator = current_app.config.get("INTERPOLATOR")
    osc_client   = current_app.config.get("OSC_CLIENT")
    addr_list    = current_app.config.get("OSC_ADDR_LIST")

    if interpolator is None or osc_client is None:
        log.warning("Interpolator/OSC client missing; drop.")
        return
    if not isinstance(addr_list, list) or not addr_list:
        log.warning("OSC_ADDR_LIST not registered; drop.")
        return

    # Compute y for UI echo (or you can reuse the return of send_data)
    y = np.asarray(interpolator.interpolate(u), dtype=float).ravel().tolist()

    # Anti-flood before egress
    if not _gate.allow(u):
        return

    # Send per-parameter using interpolator's method (updated signature)
    try:
        interpolator.send_data(osc_client, u, addr_list)
    except Exception as exc:
        log.exception("send_data failed: %s", exc)

    # Echo back to the browser
    emit("cursor_update", {"u": u, "y": y})
