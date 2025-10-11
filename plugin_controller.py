# plugin_controller_async.py
# Async OSC receiver → coalesced/rate-limited forwarder to ReaLearn
# Emits a single logical parameter: "cursor" with 3 floats [x, y, z]

from __future__ import annotations

import asyncio
import logging
import socket
import time
from collections import defaultdict
from functools import partial
from typing import Any, Dict, Iterable, List, Tuple, Union

import socketio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from constants import (
    FORWARD_PORT,
    RECEIVE_PORT,
    WEBAPP_HOST,
    WEBAPP_PORT,
    CONTROLLER_TICK_HZ,
    CONTROLLER_PER_PARAM_MIN_INTERVAL_MS,
    CONTROLLER_EPSILON,
    CONTROLLER_USE_BUNDLES,
    CONTROLLER_MAX_PER_TICK,
    CONTROLLER_MAX_PACKETS_PER_SEC,
    CONTROLLER_RECV_HOST,
)
from logger import setup_logger
from utils import load_osc_addresses

# =====================
# Module-level logger
# =====================
log = setup_logger("OSC Controller Async", level=logging.INFO)

# Type aliases for coalescible values: float or 3-vector
Scalar = float
Vec3 = Tuple[float, float, float]
Value = Union[Scalar, Vec3]



# =====================
# Utils
# =====================
class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: int | None = None) -> None:
        self.rate = float(rate_per_sec)
        self.capacity = int(capacity or max(1, int(rate_per_sec * 2)))
        self.tokens = self.capacity
        self.last = time.monotonic()

    def allow(self, cost: int = 1) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


def clip(x: float, a: float, b: float) -> float:
    return max(a, min(b, x))


def scale(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    if in_max == in_min:
        return out_min
    t = (x - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def is_seq3(v: Any) -> bool:
    return isinstance(v, (tuple, list)) and len(v) == 3


def changed_enough(prev: Value | None, new: Value, eps: float) -> bool:
    if prev is None:
        return True
    if is_seq3(prev) and is_seq3(new):
        return (abs(prev[0] - new[0]) >= eps or
                abs(prev[1] - new[1]) >= eps or
                abs(prev[2] - new[2]) >= eps)
    if not is_seq3(prev) and not is_seq3(new):
        return abs(float(prev) - float(new)) >= eps
    # Different types (scalar vs vec) → consider it changed
    return True


# =====================
# Processors (strategy)
# =====================
class BaseProcessor:
    """
    Minimal interface: updates state and, if possible, returns
    a single 'cursor' output as (key, Value) where Value = (x,y,z).
    """
    def process(self, _key: str, _val: float, _addr: str, _state: Dict[str, float]) -> List[Tuple[str, Value]]:
        return []


class TouchProcessor(BaseProcessor):
    """
    Odot → Python (touch):
      diagonal     = sqrt(screenwidth^2 + screenheight^2)
      maxRadiusPx  = diagonal * diagonalPart
      touchRadiusPx= touchradius0 * pxPerPt

      posX = clip(touch0_x, outMin, outMax)
      posY = -1 * clip(touch0_y, outMin, outMax)
      posZ = scale(touchRadiusPx, 0, maxRadiusPx, 0, outMax)

      cursor = [posX, posY, posZ] * touchcount
    """
    def process(self, _key: str, _val: float, _addr: str, state: Dict[str, float]) -> List[Tuple[str, Value]]:
        px_per_pt  = state.get("pxPerPt", 1.0)
        out_min    = state.get("outDomain_min", -1.0)
        out_max    = state.get("outDomain_max",  1.0)

        t0x = state.get("touch0_x", state.get("touch0x", 0.0))
        t0y = state.get("touch0_y", state.get("touch0y", 0.0))
        touch_radius0 = state.get("touchradius0", 0.0)
        touch_count   = state.get("touchcount", 0.0)


        # --- Z mapping: use empirical min/max so the whole virtual space is reachable ---
        # Allow overrides via state; default to measured range
        raw_min = float(state.get("touchradius_min", 9.587311))
        raw_max = float(state.get("touchradius_max", 95.96471))

        # Convert to pixels
        rmin_px = raw_min * px_per_pt
        rmax_px = raw_max * px_per_pt
        if rmax_px <= rmin_px:
            rmax_px = rmin_px + 1e-6  # Avoid zero range

        touch_radius_px = float(touch_radius0) * px_per_pt

        # Clamp then scale to [-1, 1]
        r_clamped = clip(touch_radius_px, rmin_px, rmax_px)
        pos_z = scale(r_clamped, rmin_px, rmax_px, out_min, out_max)

        pos_x = clip(float(t0x), out_min, out_max)
        pos_y = -1.0 * clip(float(t0y), out_min, out_max)

        pos_x *= touch_count
        pos_y *= touch_count
        pos_z *= touch_count

        return [("cursor", (pos_x, pos_y, pos_z))]


class ImuProcessor(BaseProcessor):
    """Placeholder: will produce ('cursor', (x,y,z)) when logic is defined."""


class OrientationProcessor(BaseProcessor):
    """Placeholder: will produce ('cursor', (x,y,z)) when logic is defined."""


def make_processor(mode: str) -> BaseProcessor:
    m = (mode or "none").lower()
    if m == "touch":
        return TouchProcessor()
    if m == "imu":
        return ImuProcessor()
    if m == "orientation":
        return OrientationProcessor()
    return BaseProcessor()


# =====================
# Coalescing forwarder
# =====================
class CoalescingForwarder:
    def __init__(
        self,
        client: SimpleUDPClient,
        osc_addresses: Dict[str, str],
        *,
        proc_mode: str = "none",
        per_param_min_interval_ms: float = CONTROLLER_PER_PARAM_MIN_INTERVAL_MS,
        tick_hz: float = CONTROLLER_TICK_HZ,
        epsilon: float = CONTROLLER_EPSILON,
        use_bundles: bool = CONTROLLER_USE_BUNDLES,
        max_per_tick: int = CONTROLLER_MAX_PER_TICK,
        max_packets_per_sec: int = CONTROLLER_MAX_PACKETS_PER_SEC,
    ) -> None:
        self.client = client
        self.addr_map = osc_addresses  # key -> OSC path expected by ReaLearn
        self.proc_mode = (proc_mode or "none").lower()
        self.min_interval = per_param_min_interval_ms / 1000.0
        self.tick_s = 1.0 / float(tick_hz)
        self.epsilon = float(epsilon)
        self.use_bundles = bool(use_bundles)
        self.max_per_tick = int(max_per_tick)
        self.pending: Dict[str, Value] = {}
        self.last_sent_ts = defaultdict(float)  # key -> last sent time
        self.last_sent_val: Dict[str, Value] = {}
        self._lock = asyncio.Lock()
        self._stop = asyncio.Event()
        self._bucket = TokenBucket(rate_per_sec=max_packets_per_sec)
        # Shared state for processors
        self.state: Dict[str, float] = {}
        self.processor = make_processor(self.proc_mode)

    def _strip_address(self, address: str) -> str | None:
        """
        Strip and normalise OSC address according to routing rules:
        - if contains 'deviceinfo' → DROP (None)
        - if contains 'fromDevice' → '/<last-segment-after-fromDevice>'
          e.g. 'ZIGSIM/fromDevice/touchcount' → '/touchcount'
        - otherwise '/<last-segment>' (e.g. '/foo/bar' → '/bar')
        """
        if not address:
            return None
        a = address.strip("/")
        if "deviceinfo" in a:
            return None
        parts = a.split("/")
        if "fromDevice" in parts:
            idx = parts.index("fromDevice")
            tail = parts[idx + 1:]
            if not tail:
                return None
            return f"/{tail[-1]}"
        return f"/{parts[-1]}"

    # ---- Ingresso OSC → (key, value) dopo lo strip ----
    def _to_updates(self, address: str, args: Tuple[Union[str, float, int], ...]) -> Iterable[Tuple[str, float]]:
        """
        Normalise incoming OSC into (key, float) updates for the internal state.

        Rules:
        - Drop any address containing 'deviceinfo'.
        - If path contains 'fromDevice', keep only the last segment: '.../fromDevice/touch0' → '/touch0'.
        - Special-case vector pairs for touch coordinates:
            '/touch0' with (x, y) → ('touch0_x', x), ('touch0_y', y)
            '/touch1' with (x, y) → ('touch1_x', x), ('touch1_y', y)
      -  If a single numeric arg remains, map to the last segment name:
          '/touchradius0' (r) → ('touchradius0', r)
          '/touchcount'   (n) → ('touchcount',   n)
        - If args look like key/value pairs (k v k v …), coerce them into (str(k), float(v)).
        """
        norm_addr = self._strip_address(address)
        if norm_addr is None:
            return []

        out: List[Tuple[str, float]] = []

        # ---- Special case: touch coordinates as a 2-float vector
        # e.g. '/touch0' (x, y) → touch0_x, touch0_y
        if norm_addr in ("/touch0", "/touch1", "/touch2", "/touch3"):
            if len(args) == 2:
                try:
                    x = float(args[0])
                    y = float(args[1])
                except Exception:
                    return []
                base = norm_addr.lstrip("/")  # 'touch0'
                out.append((f"{base}_x", x))
                out.append((f"{base}_y", y))
                return out
            # fall-through if arity is not 2 (ignore)

        # ---- Key/Value pairs (k v k v ...)
        if len(args) >= 2 and len(args) % 2 == 0:
            tmp: List[Tuple[str, float]] = []
            it = iter(args)
            while True:
                try:
                    k = next(it)
                    v = next(it)
                except StopIteration:
                    break
                try:
                    key = str(k)
                    val = float(v)
                except Exception:
                    continue
                tmp.append((key, val))
            if tmp:
                return tmp

        # ---- Single-arg → map to the last path segment
        if len(args) == 1:
            try:
                val = float(args[0])
            except Exception:
                return []
            key = norm_addr.rsplit("/", 1)[-1]
            out.append((key, val))
            return out

        return out

    # ---- Public API: aggiunge un pacchetto ricevuto ----
    async def add(self, address: str, *args: Union[str, float, int]) -> None:
        updates = list(self._to_updates(address, args))
        if not updates:
            return
        async with self._lock:
            for key, val in updates:
                # Update raw state
                self.state[key] = float(val)
                # Derived values (ideally a single ('cursor', (x,y,z)))
                derived = self.processor.process(key, float(val), address, self.state)
                if derived:
                    for k2, v2 in derived:
                        self.pending[str(k2)] = v2  # v2 can be float or (x,y,z)
                else:
                    # If processor produces nothing, don't send raw (requirement: /cursor only)
                    continue

    async def _flush_once(self) -> None:
        """
        Coalesced flush:
        - picks pending keys up to max_per_tick,
        - respects per-parameter min interval and epsilon,
        - rate-limits with a global token bucket,
        - sends OSC messages (no bundles, by design),
        - logs exactly what is being sent (path + payload) for verification.
        """
        now = time.monotonic()
        to_send: List[Tuple[str, Value]] = []

        # Collect candidates under lock
        async with self._lock:
            if not self.pending:
                return
            for key in list(self.pending.keys())[: self.max_per_tick]:
                val = self.pending.pop(key)
                last_t = self.last_sent_ts[key]
                last_v = self.last_sent_val.get(key)

                # Skip if variation is insignificant
                if not changed_enough(last_v, val, self.epsilon):
                    continue

                # Enforce per-parameter minimum interval
                if now - last_t < self.min_interval:
                    # Too soon — re-queue for a future tick
                    self.pending[key] = val
                    continue

                to_send.append((key, val))

        if not to_send:
            return

        # Send (bundles are disabled by configuration)
        for key, val in to_send:
            # Resolve OSC path; provide a sensible fallback for the canonical 'cursor'
            path = self.addr_map.get(key) or ("/cursor" if key == "cursor" else None)
            if not path:
                log.warning("UNMAPPED key=%s (drop)", key)
                continue

            # Global packet budget (token bucket)
            if not self._bucket.allow(1):
                log.debug("Global packet limit reached, message skipped")
                continue

            try:
                # Log exactly what we are about to send (path + payload)
                if is_seq3(val):
                    x, y, z = val  # type: ignore[arg-type]
                    payload = [float(x), float(y), float(z)]
                    log.info("OSC OUT %s %s", path, payload)
                    self.client.send_message(path, payload)
                else:
                    fval = float(val)
                    log.info("OSC OUT %s %s", path, fval)
                    self.client.send_message(path, fval)
            except Exception as e:
                log.warning("OSC send_message failed: %s", e)

        # Update last-sent bookkeeping
        sent_at = time.monotonic()
        for key, val in to_send:
            self.last_sent_ts[key] = sent_at
            self.last_sent_val[key] = val


    async def run(self) -> None:
        next_wake = time.monotonic()
        while not self._stop.is_set():
            await self._flush_once()
            next_wake += self.tick_s
            delay = max(0.0, next_wake - time.monotonic())
            await asyncio.sleep(delay)

    def stop(self) -> None:
        self._stop.set()


# =====================
# Bootstrapping
# =====================
async def _make_udp_client(host: str, port: int) -> SimpleUDPClient:
    """Create UDP client with increased send buffer for burst tolerance."""
    client = SimpleUDPClient(host, port)
    try:
        sock = getattr(client, "_sock", None)  # Protected access via getattr
        if sock is not None:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1 << 20)
    except Exception:
        pass
    return client


def _create_osc_handler(forwarder: CoalescingForwarder):
    """
    Factory function to create an OSC handler with forwarder bound via closure.

    This avoids global state while maintaining compatibility with python-osc Dispatcher
    which requires a synchronous handler function.

    Args:
        forwarder: The CoalescingForwarder instance to forward messages to

    Returns:
        A handler function compatible with python-osc Dispatcher
    """
    def osc_in_handler(address: str, *args):
        """
        OSC message handler for python-osc Dispatcher.
        Synchronous to match Dispatcher signature; creates async task for processing.
        """
        # Schedule async processing (non-blocking for dispatcher)
        asyncio.create_task(forwarder.add(address, *args))

    return osc_in_handler


def publish_addr_list_to_web(paths: list[str]) -> None:
    """
    Send the per-parameter OSC address list to the web-app exactly once.
    Robust variant:
      - supports both websocket and polling transports;
      - retries for a short period in case the web-app is not up yet;
      - does not block controller start-up on failure.
    """
    if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
        log.warning("addr_list publish skipped: invalid paths payload")
        return

    base_url = f"http://{WEBAPP_HOST}:{WEBAPP_PORT}"

    # Small retry loop: tolerate web-app spin-up latency.
    max_attempts = 8           # ~4–6s total depending on sleep
    sleep_secs = 0.6

    for attempt in range(1, max_attempts + 1):
        try:
            sio = socketio.Client(logger=False, engineio_logger=False)
            # Prefer websocket when available; fall back to polling if needed.
            sio.connect(
                base_url,
                transports=["websocket", "polling"],
                wait=True,
                wait_timeout=3.0,
                namespaces=["/"],   # default namespace
            )
            sio.emit("addr_list", {"paths": paths})
            # Optional: synchronous round-trip ack (non-blocking overall)
            # sio.sleep(0)  # yield once
            sio.disconnect()
            log.info("Published %d OSC parameter addresses to web-app at %s",
                     len(paths), base_url)
            return
        except Exception as e:
            if attempt == 1 and "websocket-client" in str(e).lower():
                log.warning("Install 'websocket-client' to enable WS transport: %s", e)
            if attempt < max_attempts:
                time.sleep(sleep_secs)
                continue
            log.warning("Could not publish address list to web-app after %d attempts: %s",
                        attempt, e)
            return



async def _run_async(filepath: str, proc_mode: str = "none") -> None:
    """
    Async entry point for the OSC controller.

    Args:
        filepath: Path to JSON file containing OSC address mappings
        proc_mode: Processing mode ('none', 'touch', 'imu', 'orientation')
    """
    log.info(
        "Receiving OSC on %d and forwarding to web on %d | proc_mode=%s",
        RECEIVE_PORT, FORWARD_PORT, proc_mode,
    )

    # 1) Load logical->OSC path map and prepare ordered list for web app
    raw = load_osc_addresses(filepath)
    if isinstance(raw, list):
        # List already in parameter y order
        addr_list_for_web: list[str] = [str(p) for p in raw]
        # Map key->path: '/plugin/cursor' → 'cursor'
        osc_addresses: Dict[str, str] = {addr.rsplit("/", 1)[-1]: addr for addr in raw}
    elif isinstance(raw, dict):
        # Dictionary: forwarder uses key->path as-is
        osc_addresses = {str(k): str(v) for k, v in raw.items()}
        # List for web app derived from values (watch ordering!)
        addr_list_for_web = list(osc_addresses.values())
        log.warning(
            "Address file is a dict: ensure value order matches 'y' indices (len=%d).",
            len(addr_list_for_web)
        )
    else:
        osc_addresses = {}
        addr_list_for_web = []

    if not osc_addresses:
        log.warning("osc_addresses is empty – nothing will be forwarded!")

    # Ensure canonical path for logical cursor
    osc_addresses.setdefault("cursor", "/cursor")

    # 2) Publish address list to web app (one-time, non-blocking)
    publish_addr_list_to_web(addr_list_for_web)

    # 3) Sender: controller → web app (OSC) on FORWARD_PORT
    client = await _make_udp_client("127.0.0.1", FORWARD_PORT)
    forwarder = CoalescingForwarder(client, osc_addresses, proc_mode=proc_mode)

    # 4) Receiver: device/software → controller (OSC) on RECEIVE_PORT
    loop = asyncio.get_running_loop()
    dispatcher = Dispatcher()

    # Create handler with forwarder bound via closure (no global state)
    handler = _create_osc_handler(forwarder)
    dispatcher.map("/interpolated_data", handler)
    dispatcher.set_default_handler(handler)

    try:
        server = AsyncIOOSCUDPServer((CONTROLLER_RECV_HOST, RECEIVE_PORT), dispatcher, loop)
        transport, _protocol = await server.create_serve_endpoint()
        log.info("OSC server bound on %s:%d (listening)", CONTROLLER_RECV_HOST, RECEIVE_PORT)
    except OSError as e:
        log.error("Cannot bind UDP %s:%s. Check port availability. %s", CONTROLLER_RECV_HOST, RECEIVE_PORT, e)
        return

    forward_task = asyncio.create_task(forwarder.run())

    try:
        await asyncio.Event().wait()  # Run forever
    except (KeyboardInterrupt, SystemExit):
        log.info("Shutting down…")
    finally:
        forwarder.stop()
        await asyncio.wait({forward_task}, timeout=1.0)
        transport.close()