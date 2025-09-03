// /static/js/core.js
// ============================================================
// Central state, constants, DOM helpers and utilities
// ============================================================

// -----------------------------
// Global state shared across modules
// -----------------------------
export const state = {
  // Data & meta (latent in [0,1])
  latent: [],            // NxD
  dim: 0,                // D
  boundsMin: [],
  boundsMax: [],
  axisNames: [],         // ["x","y","z","w"]
  presetNames: [],

  // Views / axes
  currentAxes:  { x: 0, y: 1, z: 2 },   // 2D/3D
  currentAxesA: { x: 0, y: 1 },         // 4D view A
  currentAxesB: { x: 2, y: 3 },         // 4D view B
  is3D: false,

  // Cursor & camera
  cursorPoint: null,     // [0,1]^D (real/data-space)
  lastCamera: null,

  // Input
  inputSource: "keyboard",
  uCurrent: [],          // [-1,1]^D  (navigation-space)
  uTarget:  [],

  // Timers / gates
  _lastSendMs: 0,
};

// -----------------------------
// Axis naming
// -----------------------------
export function buildAxisNames(n) {
  const std = ["x", "y", "z", "w"];
  state.axisNames = std.slice(0, n);
}

// -----------------------------
// Generic utils
// -----------------------------
export function clamp(v, lo, hi){ return Math.max(lo, Math.min(hi, v)); }
export function clamp01(v){ return clamp(v, 0, 1); } // legacy
export function getColumn(mat, j){ return (mat || []).map(row => row[j]); }

export function lerp(a, b, t){ return a + (b - a) * t; }
export const mix = lerp;
export function vecLerp(a, b, t){
  const n = Math.min(a.length, b.length);
  const out = new Array(n);
  for (let i = 0; i < n; i++) out[i] = lerp(a[i], b[i], t);
  return out;
}
export function assignVecLerp(out, a, b, t){
  const n = Math.min(out.length, a.length, b.length);
  for (let i = 0; i < n; i++) out[i] = lerp(a[i], b[i], t);
  return out;
}
export function almostEqual(a, b, eps = 1e-9){ return Math.abs(a - b) <= eps; }

export function timeNowMs(){ return (typeof performance !== "undefined" && performance.now) ? performance.now() : Date.now(); }
export function shouldSend(ms){
  const now = timeNowMs();
  if (now - state._lastSendMs >= ms){
    state._lastSendMs = now;
    return true;
  }
  return false;
}

// Step size from modifiers (used by keyboard handler)
export function currentStep(e){
  if (e && e.shiftKey) return CONST.STEP_COARSE;
  if (e && e.altKey)   return CONST.STEP_FINE;
  return CONST.STEP_BASE;
}

// -----------------------------
// Space conversions
//   u ∈ [-1,1]^D   (navigation / visualization)
//   l ∈ [lo,hi]^D  (data-space; tipicamente [0,1])
// -----------------------------
export function uToLatent(u, dimIdx){
  const uu = clamp(Number.isFinite(u) ? u : 0, -1, 1);
  const lo = state.boundsMin[dimIdx], hi = state.boundsMax[dimIdx];
  const span = Math.max(1e-12, (hi - lo));
  return (uu + 1) * 0.5 * span + lo;
}
export function latentToU(v, dimIdx){
  const lo = state.boundsMin[dimIdx], hi = state.boundsMax[dimIdx];
  const span = Math.max(1e-12, (hi - lo));
  const u = 2 * ((v - lo) / span) - 1;
  return clamp(u, -1, 1);
}

// ============================================================
// THEME bridge (CSS variables only, no JS fallbacks)
// ============================================================
function _cssVar(name){
  const s = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if (!s) {
    console.error(`[theme] Missing CSS variable ${name}. Define it in visualizer_style.css :root{ ${name}: ... }`);
    throw new Error(`Missing CSS variable ${name}`);
  }
  return s;
}
function _cssNumber(name){
  const s = _cssVar(name);
  const n = parseFloat(s);
  if (!Number.isFinite(n)) {
    console.error(`[theme] CSS variable ${name} must be a number, got: "${s}"`);
    throw new Error(`CSS variable ${name} is not numeric`);
  }
  return n;
}
export function ensureCssTheme(){
  // Touch getters to validate presence/types at startup
  void CONST.CURSOR_GLOW_SIZE;
  void CONST.CURSOR_GLOW_COLOR;
  void CONST.CURSOR_GLOW_OPACITY;
  void CONST.CURSOR_DOT_SIZE;
  void CONST.CURSOR_DOT_COLOR;
  void CONST.CURSOR_DOT_LINE;
  void CONST.MARKER_COLOR;
  void CONST.BG_COLOR;
}

// -----------------------------
// Constants
// - Theme values: from CSS (getters).
// - Behavior values: JS numbers (single source of truth).
// -----------------------------
export const CONST = {
  // THEME (from CSS)
  get CURSOR_GLOW_SIZE()    { return _cssNumber("--cursor-glow-size"); },
  get CURSOR_GLOW_COLOR()   { return _cssVar("--cursor-glow-color"); },
  get CURSOR_GLOW_OPACITY() { return _cssNumber("--cursor-glow-opacity"); },
  get CURSOR_DOT_SIZE()     { return _cssNumber("--cursor-dot-size"); },
  get CURSOR_DOT_COLOR()    { return _cssVar("--cursor-dot-color"); },
  get CURSOR_DOT_LINE()     { return _cssVar("--cursor-dot-line"); },
  get MARKER_COLOR()        { return _cssVar("--marker-color"); },
  get BG_COLOR()            { return _cssVar("--plot-bg"); },

  // BEHAVIOR (logic/timing) — keep in JS
  STEP_BASE: 0.03,
  STEP_FINE: 0.01,
  STEP_COARSE: 0.1,
  LERP_ALPHA: 0.35,
  SEND_INTERVAL_MS: 60,
  MOVE_EPS: 1e-3,
};

// ============================================================
// DOM helpers (kept here to avoid duplication in ui.js/main.js)
// ============================================================

/**
 * Populate a <select> with options.
 * @param {HTMLSelectElement} sel - the select element
 * @param {Array<{value:string,label:string}>|string[]} options - items
 * @param {string|number|null} selected - optional value to select (or index number)
 * @param {boolean} clear - clear current options (default true)
 */
export function populateSelect(sel, options, selected = null, clear = true){
  if (!sel) return;
  if (clear) sel.innerHTML = "";

  const norm = (Array.isArray(options) ? options : []);
  norm.forEach((opt, i) => {
    const o = document.createElement("option");
    if (typeof opt === "object" && opt && "value" in opt) {
      o.value = String(opt.value);
      o.textContent = String(opt.label ?? opt.value);
    } else {
      o.value = String(opt);
      o.textContent = String(opt);
    }
    sel.appendChild(o);
  });

  if (selected != null) {
    // allow index or value
    if (typeof selected === "number" && selected >= 0 && selected < sel.options.length) {
      sel.selectedIndex = selected;
    } else {
      sel.value = String(selected);
    }
  }
}

/**
 * Update controls visibility based on dimensionality.
 * Shows single-axis controls for 2D/3D; dual-axis controls for 4D.
 * Also toggles .z-only (Z selector) only when dim===3.
 */
export function updateControlsVisibility(dim){
  const single = document.getElementById("single-axis-controls");
  const dual   = document.getElementById("dual-axis-controls");
  // legacy W slice removed entirely elsewhere

  if (dim <= 3) {
    if (single) single.style.display = "";
    if (dual)   dual.style.display   = "none";
  } else {
    if (single) single.style.display = "none";
    if (dual)   dual.style.display   = "block";
  }

  // Show Z selector only in 3D
  const zEls = document.querySelectorAll(".z-only");
  zEls.forEach(el => {
    el.style.display = (dim === 3) ? "" : "none";
  });
}

/**
 * Build axis options array like ["x","y","z","w"] for a given dimension.
 * @param {number} n
 * @returns {string[]}
 */
export function axisOptions(n){
  return ["x","y","z","w"].slice(0, n);
}

/**
 * Sync axis <select> elements with current axis names.
 * @param {HTMLSelectElement} selX
 * @param {HTMLSelectElement} selY
 * @param {HTMLSelectElement|null} selZ
 */
export function syncAxisSelectors(selX, selY, selZ = null){
  const opts = axisOptions(state.dim);
  populateSelect(selX, opts, state.axisNames[0] ?? "x");
  populateSelect(selY, opts, state.axisNames[1] ?? "y");
  if (selZ) populateSelect(selZ, opts, state.axisNames[2] ?? "z");
}

/**
 * Utility: read CSS theme variables at runtime and return an object.
 * (Handy if you need to pass theme into Plotly templates, etc.)
 */
export function readTheme(){
  return {
    markerColor:   CONST.MARKER_COLOR,
    cursorGlow:    { size: CONST.CURSOR_GLOW_SIZE, color: CONST.CURSOR_GLOW_COLOR, opacity: CONST.CURSOR_GLOW_OPACITY },
    cursorDot:     { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: CONST.CURSOR_DOT_LINE },
    bg:            CONST.BG_COLOR,
  };
}
