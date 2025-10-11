# visualizer.py
# -----------------------------------------------------------------------------
# Visualiser: Receives OSC '/cursor [x y z]' from controller and updates the
# browser UI via Socket.IO with 'cursor_update' event {u, y}.
#
# Important:
# - This module does NOT send anything to ReaLearn. Egress to ReaLearn happens
#   ONLY in the web app's socket handler (socket_handlers.cursor_move),
#   which applies anti-flood throttling and uses per-parameter address lists.
#
# - Maintains both async (run) and background threaded (start) versions for
#   compatibility. No nested functions.
# -----------------------------------------------------------------------------

from __future__ import annotations

import asyncio
import threading
from typing import List, Tuple, Union, Optional

import numpy as np
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from constants import (
    IP_ADDRESS,     # tipicamente usato per il bind/host locale del visualiser
    FORWARD_PORT,   # porta OSC su cui il visualiser riceve il /cursor dal controller
)

from logger import setup_logger

log = setup_logger("Visualizer")

Number = Union[int, float]


def _coerce_cursor(args: Tuple[Union[str, Number], ...]) -> List[float]:
    """
    Coerce an arbitrary OSC payload into a 3D cursor [x, y, z].

    Policy (British English):
      - Accept 2D or 3D vectors; pad z=0.0 if missing.
      - Coerce each element to float.
      - Return [] if coercion fails or the arity is not meaningful.
    """
    try:
        vec = [float(a) for a in args]
    except Exception:
        return []

    if not vec:
        return []
    if len(vec) >= 3:
        return vec[:3]
    if len(vec) == 2:
        return [vec[0], vec[1], 0.0]
    return []  # single value is not meaningful for a 2D/3D cursor


class Visualize:
    """
    Minimal OSC → UI bridge for visualisation:

        controller  ──(OSC '/cursor [x y z]')──>  Visualize
        Visualize   ──(Socket.IO 'cursor_update')──>  Browser

    Responsibilities:
      • Compute y = interpolator.interpolate(u) for UI feedback only.
      • Emit {'u': u, 'y': y} as 'cursor_update' to the browser.

    Non-responsibilities:
      • Do NOT send anything to ReaLearn here (handled in socket_handlers.py).
    """

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def __init__(self, latent_data: np.ndarray, socketio) -> None:
        """
        Parameters
        ----------
        latent_data : np.ndarray
            Optional dataset used for UI context (plots, guides, etc.).
        socketio : flask_socketio.SocketIO
            Server instance to notify the browser in real time.
        """
        self.latent = latent_data
        self.socketio = socketio

        # Runtime members set in run()/start()
        self._interpolator = None            # set in run()
        self._server_transport = None        # AsyncIOUDP transport
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._stop_ev: Optional[asyncio.Event] = None

        # Thread support (optional background runner)
        self._thread: Optional[threading.Thread] = None

    # -------------------------------------------------------------------------
    # Public API (Threaded)
    # -------------------------------------------------------------------------

    def start(self, host: str = IP_ADDRESS, port: int = FORWARD_PORT, *,
              interpolator=None, _osc_client_unused=None) -> None:
        """
        Start the visualiser in a background thread.
        Notes (British English):
          - `interpolator` is required to compute 'y' for the UI.
          - `_osc_client_unused` is kept for compatibility; it is not used.
          - The server binds to (host, port) and runs until `stop()` is called.
        """
        if self._thread is not None:
            log.warning("Visualizer already running; ignoring second start()")
            return

        def _thread_main():
            try:
                asyncio.run(self.run(host, port, interpolator, _osc_client_unused))
            except Exception as e:
                log.error("Visualizer thread crashed: %s", e)

        self._thread = threading.Thread(target=_thread_main, name="VisualizerThread", daemon=True)
        self._thread.start()
        log.info("Visualizer thread started on %s:%d", host, port)

    def stop(self, timeout: float = 1.0) -> None:
        """
        Request graceful shutdown if running in threaded mode.
        It signals the async loop event and joins the background thread.
        """
        if self._loop is not None and self._stop_ev is not None:
            # Signal stop on the loop thread
            self._loop.call_soon_threadsafe(self._stop_ev.set)

        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
            log.info("Visualizer thread joined")

    # -------------------------------------------------------------------------
    # Public API (Async)
    # -------------------------------------------------------------------------

    async def run(self, host: str, port: int, interpolator, _osc_client_unused=None) -> None:
        """
        Start the OSC server and run until asked to stop.

        Notes (British English):
          - This is the canonical async runner (awaited by the orchestrator).
          - The 'interpolator' is used ONLY for UI feedback; there is no OSC egress here.
          - '_osc_client_unused' is intentionally ignored to keep the signature
            compatible with older call sites.
        """
        self._interpolator = interpolator
        self._loop = asyncio.get_running_loop()
        self._stop_ev = asyncio.Event()

        dispatcher = Dispatcher()

        # Register a bound method (sync) as per python-osc expectations; it will
        # schedule the actual async processing on the event loop.
        dispatcher.map("/cursor", self.on_osc_sync)
        dispatcher.set_default_handler(self.on_osc_sync)

        try:
            server = AsyncIOOSCUDPServer((host, port), dispatcher, self._loop)
            transport, _ = await server.create_serve_endpoint()
            self._server_transport = transport
            log.info("Visualizer OSC server bound on %s:%d (listening)", host, port)
        except OSError as e:
            log.error("Visualizer cannot bind UDP %s:%d. %s", host, port, e)
            return

        try:
            # Park here until stop() signals the event (threaded) or forever (awaited).
            await self._stop_ev.wait()
        except (KeyboardInterrupt, SystemExit):
            log.info("Visualizer shutting down…")
        finally:
            try:
                if self._server_transport is not None:
                    self._server_transport.close()
            finally:
                self._server_transport = None
                self._loop = None
                self._stop_ev = None

    # -------------------------------------------------------------------------
    # OSC handling (no nested defs)
    # -------------------------------------------------------------------------

    def on_osc_sync(self, address: str, *args) -> None:
        """
        Synchronous entrypoint required by python-osc's Dispatcher.
        We do minimal work here and schedule the async handler on the event loop.
        """
        if address != "/cursor" and not address.endswith("/cursor"):
            return  # ignore non-cursor traffic quietly

        # Coerce payload to [x, y, z]
        u = _coerce_cursor(args)
        if not u:
            return

        # Schedule the async handler; tolerate both threaded and awaited modes.
        if self._loop is None:
            # If no loop is known yet (should not happen after run/start), ignore.
            return
        asyncio.run_coroutine_threadsafe(self._handle_cursor(u), self._loop)

    async def _handle_cursor(self, u: List[float]) -> None:
        """
        Async processing of a cursor update:
          - Interpolate for UI feedback.
          - Emit 'cursor_update' to the browser.
        """
        try:
            y = self._interpolator.interpolate(u) if self._interpolator is not None else []
            u_list = np.asarray(u, dtype=float).ravel().tolist()
            y_list = np.asarray(y, dtype=float).ravel().tolist()
        except Exception as e:
            log.error("Visualizer interpolate failed: %s", e)
            return

        # Notify the browser UI; front-end may optionally forward back to the
        # server's socket handler which deals with ReaLearn (anti-flood etc.).
        self.socketio.emit("cursor_update", {"u": u_list, "y": y_list})


# -----------------------------------------------------------------------------
# Optional convenience utilities for quick startup using project constants.
# -----------------------------------------------------------------------------

def start_visualizer_thread(visualizer: Visualize, interpolator) -> None:
    """
    Convenience helper to start the visualiser on (IP_ADDRESS, FORWARD_PORT)
    in a background thread using project constants.
    """
    visualizer.start(IP_ADDRESS, FORWARD_PORT, interpolator=interpolator)


async def run_visualizer_async(visualizer: Visualize, interpolator) -> None:
    """
    Convenience helper to await the visualiser on (IP_ADDRESS, FORWARD_PORT)
    using project constants.
    """
    await visualizer.run(IP_ADDRESS, FORWARD_PORT, interpolator, _osc_client_unused=None)
