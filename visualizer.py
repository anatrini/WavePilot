"""
Server-side bridge for OSC-controlled latent navigation (2–4D).

Responsibilities:
  - Keep latent metadata (N × d, with 2 ≤ d ≤ 4).
  - Listen to OSC cursor updates as k values in [-1, 1]^d.
  - Forward the normalised cursor to the RBF interpolator (which performs mapping/clipping).
  - Echo the cursor to the browser via Socket.IO as 'cursor_update' so the Plotly marker stays in sync.

Notes:
  - The Flask web server and Socket.IO lifecycle live in train.py.
  - Mouse-driven updates originate in the browser and are handled in train.py
    via the 'cursor_move' Socket.IO event. This module focuses on OSC → server → UI.
"""

from __future__ import annotations

import asyncio
from threading import Thread
from typing import Optional

import numpy as np
from pythonosc import dispatcher as osc_dispatcher
from pythonosc import osc_server

from logger import setup_logger
from constants import VIZ_MIN, VIZ_MAX, MIN_LATENT_DIM, MAX_LATENT_DIM


log = setup_logger("Visualizer")


class Visualize:
    """
    OSC bridge for Plotly-based latent visualisation.

    Parameters
    ----------
    data : np.ndarray of shape (N, d)
        Latent coordinates used by the client (must match the latent space used by RBF).
        d must be in {2, 3, 4}.
    socketio : object
        An object exposing 'emit(event, payload)' (e.g., Flask-SocketIO instance).

    Behaviour
    ---------
    - Incoming OSC cursor values are expected as k floats in [-1, 1].
      They are clamped and resized to match d (drop extras, pad missing with 0.0).
    - The same values are dispatched to:
        (1) interpolator.send_data(osc_client, u_list)   # u ∈ [-1,1]^d
        (2) socketio.emit('cursor_update', {'u': u_list})
    """
        
    def __init__(self, data: np.ndarray, socketio) -> None:
        
        Z = np.asarray(data, dtype=float)
        assert Z.ndim == MIN_LATENT_DIM and MIN_LATENT_DIM <= Z.shape[1] <= MAX_LATENT_DIM # Latent data must be [N, d] with 2 ≤ d ≤ 4.

        self.data = Z
        self.dim = int(Z.shape[1])

        # Per-dimension bounds (kept for reference if needed server-side)
        self.bounds_min = Z.min(axis=0)
        self.bounds_max = Z.max(axis=0)

        self.socketio = socketio

        # Runtime dependecies set at run()
        self._interpolator = None
        self._osc_client = None

        # OSC server internals
        self._osc_server: Optional[osc_server.ThreadingOSCUDPServer] = None
        self._osc_thread: Optional[Thread] = None
        self._running = False

    # ----------------------------- public API -----------------------------
    async def run(self, listen_ip: str, listen_port: int, interpolator, osc_client) -> None:
        """
        Start the OSC listener in a background thread and keep the coroutine alive.

        Parameters
        ----------
        listen_ip : str
            IP to bind the OSC server (e.g., '127.0.0.1').
        listen_port : int
            Port to bind the OSC server (device → this process).
        interpolator : RBFInterpolation
            Instance exposing send_data(osc_client, u_list) where u ∈ [-1,1]^d.
        osc_client : pythonosc.udp_client.SimpleUDPClient
            Destination for sending interpolated data as OSC messages.
        """
        self._interpolator = interpolator
        self._osc_client = osc_client

        self._start_osc_server(listen_ip, listen_port)

        self._running = True
        try:
            while self._running:
                await asyncio.sleep(0.1)
        finally:
            self._stop_osc_server()

    def stop(self) -> None:
        """Request a graceful stop; the awaiting task will close the OSC server."""
        self._running = False


    # --------------------------- OSC plumbing ----------------------------
    def _start_osc_server(self, ip: str, port: int) -> None:
        disp = osc_dispatcher.Dispatcher()

        # Generic cursor route: expects k floats in [-1,1]; k will be resized to match d.
        disp.map("/cursor", self._on_osc_cursor)

        # If your device uses different addresses, add more mappings here:
        # disp.map("/device/cursor", self._on_osc_cursor)

        srv = osc_server.ThreadingOSCUDPServer((ip, port), disp)
        self._osc_server = srv

        th = Thread(target=srv.serve_forever, name="OSCServerThread", daemon=True)
        th.start()
        self._osc_thread = th

        log.info("OSC server listening on %s:%s", ip, port)

    def _stop_osc_server(self) -> None:
        if self._osc_server is not None:
            try:
                self._osc_server.shutdown()
                log.info("OSC server shutdown requested!")
            except Exception as exc:
                log.error("OSC server shutdown error: %s", str(exc))
        if self._osc_thread is not None:
            try:
                self._osc_thread.join(timeout=2.0)
            except Exception:
                pass
        
        self._osc_server = None
        self._osc_thread = None


    # --------------------------- event handlers --------------------------
    def _on_osc_cursor(self, unused_addr: str, *args) -> None:
        """
        Handle OSC cursor updates coming from an external device.

        Args are interpreted as k floats in [-1, 1]. The vector is resized to self.dim:
          - extra values are dropped,
          - missing values are padded with 0.0 (centre in normalised space).

        The normalised cursor is then:
          1) forwarded to the RBF interpolator (send_data),
          2) echoed to the browser as 'cursor_update'.
        """
        u = np.asarray(args, dtype=float).ravel()

        # Resize to latent dimensionality
        if u.size > self.dim:
            u = u[: self.dim]
        elif u.size < self.dim:
            pad = self.dim - u.size
            u = np.pad(u, (0, pad), mode="constant", constant_values=0.0)

        # Clamp to [-1, 1] for robustness
        u = np.clip(u, VIZ_MIN, VIZ_MAX)

        # 1. interpolation -> OSC
        try:
            if self._interpolator is not None and self._osc_client is not None:
                self._interpolator.send_data(self._osc_client, u.tolist())
        except Exception as exc:
            log.error("Interpolator send_data failed: %s", str(exc))

        # 2. Echo to UI
        try:
            self.socketio.emit("cursor_update", {"u": u.tolist()})
        except Exception as exc:
            log.error("SocketIO emit failed: %s", str(exc))
