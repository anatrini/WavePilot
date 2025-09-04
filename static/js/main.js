// main.js — entry point

import { state, CONST, clamp, buildAxisNames, uToLatent } from "./core.js";
import { drawPlots, updateCursor } from "./plot.js";
import { setupAxisSelectors, refreshShortcuts, dom as UI, setupDual2DControls } from "./ui.js";
import { setupSocket, sendCursor } from "./net.js";

// -------------------- Keyboard handling --------------------

// Currently pressed keys
const keysDown = new Set();
// Modifier flags
const modifiers = { shift: false, alt: false };

// Keys we care about
const ALLOWED_KEYS = new Set(["a","d","w","s","f","h","t","g","q","e","shift","alt"]);

// Normalise key across layouts using event.code when available
function normKey(e) {
  const k = (e.key  || "").toLowerCase();
  const c = (e.code || "").toLowerCase();
  const map = { keya:"a", keyd:"d", keyw:"w", keys:"s", keyf:"f", keyh:"h", keyt:"t", keyg:"g", keyq:"q", keye:"e" };
  return map[c] || k;
}

function handleKeyDown(e) {
  if (state.inputSource !== "keyboard") return;
  const tag = (e.target && e.target.tagName || "").toLowerCase();
  // Allow shortcuts while focus is on <select>; only suppress for text inputs
  if (tag === "input" || tag === "textarea") return;

  const k = normKey(e);
  if (!ALLOWED_KEYS.has(k)) return;

  e.preventDefault();
  keysDown.add(k);
  if (k === "shift") modifiers.shift = true;
  if (k === "alt")   modifiers.alt   = true;
}

function handleKeyUp(e) {
  const k = normKey(e);
  keysDown.delete(k);
  if (k === "shift") modifiers.shift = false;
  if (k === "alt")   modifiers.alt   = false;
}

function attachKeyListeners() {
  window.addEventListener("keydown", handleKeyDown, { passive: false });
  window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
}
function detachKeyListeners() {
  window.removeEventListener("keydown", handleKeyDown);
  window.removeEventListener("keyup",   handleKeyUp);
}

// Step size based on modifiers
function stepFromModifiers() {
  if (modifiers.shift) return CONST.STEP_COARSE;
  if (modifiers.alt)   return CONST.STEP_FINE;
  return CONST.STEP_BASE;
}

// Apply keyboard deltas into state.uTarget (u-space in [-1,1])
function applyKeyboardInput() {
  if (keysDown.size === 0) return;

  const step = stepFromModifiers();
  const u = state.uTarget.slice(); // accumulate from current target

  const add = (idx, d) => {
    if (Number.isFinite(idx)) u[idx] = clamp(u[idx] + d, -1, 1);
  };

  switch (Number(state.dim)) {
    case 4: {
      const a = state.currentAxesA || { x: 0, y: 1 };
      const b = state.currentAxesB || { x: 2, y: 3 };
      if (keysDown.has("a")) add(a.x, -step);
      if (keysDown.has("d")) add(a.x,  step);
      if (keysDown.has("w")) add(a.y,  step);
      if (keysDown.has("s")) add(a.y, -step);
      if (keysDown.has("f")) add(b.x, -step);
      if (keysDown.has("h")) add(b.x,  step);
      if (keysDown.has("t")) add(b.y,  step);
      if (keysDown.has("g")) add(b.y, -step);
      break;
    }
    case 3: {
      const ax = Number(state.currentAxes.x);
      const ay = Number(state.currentAxes.y);
      const az = Number(state.currentAxes.z);
      if (keysDown.has("a")) add(ax, -step);
      if (keysDown.has("d")) add(ax,  step);
      if (keysDown.has("w")) add(ay,  step);
      if (keysDown.has("s")) add(ay, -step);
      if (keysDown.has("q")) add(az,  step);  // Z+ towards the observer
      if (keysDown.has("e")) add(az, -step);  // Z- away
      break;
    }
    default: {
      const ax = Number(state.currentAxes.x);
      const ay = Number(state.currentAxes.y);
      if (keysDown.has("a")) add(ax, -step);
      if (keysDown.has("d")) add(ax,  step);
      if (keysDown.has("w")) add(ay,  step);
      if (keysDown.has("s")) add(ay, -step);
      break;
    }
  }

  state.uTarget = u;
}

// -------------------- Animation / smoothing --------------------

let lastSentMs = 0;

function tickSmooth(ts) {
  // 1) Read keyboard every frame (no-op if nothing pressed)
  applyKeyboardInput();

  // 2) Lerp towards target
  let moved = false;
  for (let j = 0; j < state.uCurrent.length; j++) {
    const u0 = state.uCurrent[j];
    const ut = state.uTarget[j];
    const u1 = u0 + (ut - u0) * CONST.LERP_ALPHA;
    if (Math.abs(u1 - u0) > CONST.MOVE_EPS) moved = true;
    state.uCurrent[j] = u1;
  }

  // 3) If moved enough, update cursor & maybe send to backend
  if (moved) {
    // Convert u -> latent data-space for the visualiser & server
    const lp = state.uCurrent.map((uu, j) => uToLatent(uu, j));
    updateCursor(lp);

    const now = performance.now();
    if (now - lastSentMs >= CONST.SEND_INTERVAL_MS) {
      lastSentMs = now;
      sendCursor(lp);
    }
  }

  requestAnimationFrame(tickSmooth);
}

// -------------------- Boot --------------------

(async function init() {
  // 1) Fetch data/meta
  const resp = await fetch("/data");
  const meta = await resp.json();

  // Normalise and assign core state
  state.latent    = Array.isArray(meta.latent) ? meta.latent : [];
  state.dim       = Number(meta.dim) || 0;
  state.boundsMin = Array.isArray(meta.bounds_min) ? meta.bounds_min : [];
  state.boundsMax = Array.isArray(meta.bounds_max) ? meta.bounds_max : [];

  // Preset names: server or fallback ID1..N
  const N = state.latent.length;
  const fromServer = Array.isArray(meta.preset_names) ? meta.preset_names : [];
  state.presetNames = Array.from({ length: N }, (_, i) => {
    const s = (fromServer[i] == null ? "" : String(fromServer[i]).trim());
    return s ? s : `ID${i + 1}`;
  });

  // Safety: recompute bounds from actual data
  if (N > 0) {
    const d = state.dim;
    const bmin = new Array(d).fill(+Infinity);
    const bmax = new Array(d).fill(-Infinity);
    for (const row of state.latent) {
      for (let j = 0; j < d; j++) {
        const v = row[j];
        if (v < bmin[j]) bmin[j] = v;
        if (v > bmax[j]) bmax[j] = v;
      }
    }
    state.boundsMin = bmin;
    state.boundsMax = bmax;
  }

  // Axis names and sensible defaults
  buildAxisNames(state.dim);
  if (state.dim === 4) {
    state.currentAxesA = { x: 0, y: 1 };
    state.currentAxesB = { x: 2, y: 3 };
  }

  // Initialise u/cursor (centre of the cube) and map to data-space
  state.uCurrent    = new Array(state.dim).fill(0.0);
  state.uTarget     = new Array(state.dim).fill(0.0);
  state.cursorPoint = state.uCurrent.map((uu, j) => uToLatent(uu, j));

  // Reflect dimensionality in the shortcuts panel and populate axis selectors
  refreshShortcuts();
  setupAxisSelectors();

  // Input source wiring
  if (UI.selInput) {
    state.inputSource = UI.selInput.value || "keyboard";
    if (state.inputSource === "keyboard") attachKeyListeners();
    else                                   detachKeyListeners();
    refreshShortcuts();

    UI.selInput.addEventListener("change", () => {
      state.inputSource = UI.selInput.value;
      if (state.inputSource === "keyboard") attachKeyListeners();
      else                                   detachKeyListeners();
      refreshShortcuts();
    });
  }

  // Populate preset dropdown
  const selPoint = document.getElementById("preset-select");
  if (selPoint) {
    selPoint.innerHTML = '<option value="">— select preset —</option>';
    for (let i = 0; i < state.presetNames.length; i++) {
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = state.presetNames[i];
      selPoint.appendChild(opt);
    }
    selPoint.addEventListener("change", () => {
      const v = selPoint.value;
      if (v === "") return;
      const idx = Number(v);
      if (!Number.isFinite(idx) || idx < 0 || idx >= state.latent.length) return;
      const lp = state.latent[idx].slice();  // data-space
      state.cursorPoint = lp;
      // sync uCurrent/uTarget with this point
      for (let j = 0; j < state.dim; j++) {
        const lo = state.boundsMin[j], hi = state.boundsMax[j];
        const u = (lo === hi) ? 0 : ((lp[j] - lo) / (hi - lo)) * 2 - 1;
        state.uCurrent[j] = state.uTarget[j] = clamp(u, -1, 1);
      }
      updateCursor(lp);
      sendCursor(lp);
    });
  }

  // Initial draw
  drawPlots();
  updateCursor(state.cursorPoint);

  // 4D convenience (optional)
  if (state.dim === 4 && typeof setupDual2DControls === "function") {
    setupDual2DControls();
    const leftEl  = document.getElementById("plot-left");
    const rightEl = document.getElementById("plot-right");
    if (leftEl)  leftEl.addEventListener("click", () => { window.activeView = "A"; });
    if (rightEl) rightEl.addEventListener("click", () => { window.activeView = "B"; });
  }

  // Start loop
  requestAnimationFrame(tickSmooth);

  // Socket wiring
  setupSocket((lp) => {
    state.cursorPoint = lp;
    // also update u-space to follow external updates
    for (let j = 0; j < state.dim; j++) {
      const lo = state.boundsMin[j], hi = state.boundsMax[j];
      const u = (lo === hi) ? 0 : ((lp[j] - lo) / (hi - lo)) * 2 - 1;
      state.uCurrent[j] = state.uTarget[j] = clamp(u, -1, 1);
    }
    updateCursor(lp);
  });
})();
