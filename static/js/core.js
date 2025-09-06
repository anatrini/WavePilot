// core.js — app core (state + pure utilities). No visual styling here.

/* =========================================================
   Global state (shared across modules)
   ========================================================= */
export const state = {
  // data / meta
  latent: [],            // NxD array in [0,1]
  dim: 0,                // 2 | 3 | 4
  boundsMin: [],         // per-dimension lower bounds (usually 0)
  boundsMax: [],         // per-dimension upper bounds (usually 1)
  presetNames: [],       // labels for points (ID1..N if absent)
  axisNames: [],         // ['x','y','z','w'] (subset by dim)

  // current views (indices into latent dims)
  currentAxes:  { x: 0, y: 1, z: 2 },   // used in 2D/3D
  currentAxesA: { x: 0, y: 1 },         // used in 4D (left view)
  currentAxesB: { x: 2, y: 3 },         // used in 4D (right view)

  // cursor traces indices (set by plot.js after rendering)
  cursorLeft:  null,     // {glowIdx, dotIdx}
  cursorRight: null,

  // navigation
  inputSource: "keyboard", // 'keyboard' | 'mouse' | 'osc'
  uCurrent: [],           // smoothed cursor in u-space [-1,1]
  uTarget:  [],           // target cursor in u-space [-1,1]
  cursorPoint: [],        // current latent point in [0,1]

  // keyboard focus for 4D (which 2D view to steer first)
  activeView: "A",        // 'A' | 'B'
};

/* Exposed containers for plots */
export function els() {
  return {
    left:  document.getElementById("plot-left"),
    right: document.getElementById("plot-right"),
  };
}

/* =========================================================
   Constants (logic only — no styling here)
   ========================================================= */
export const CONST = {
  STEP_BASE:       0.03,    // default step in u-space
  STEP_FINE:       0.01,    // with Alt
  STEP_COARSE:     0.10,    // with Shift
  LERP_ALPHA:      0.35,    // smoothing factor for uCurrent←uTarget
  SEND_INTERVAL_MS: 60,     // throttle for socket emits
  MOVE_EPS:        1e-3,    // deadzone for movement
};

/* Keyboard state shared across modules */
export const keysDown = new Set();

/* Derive current step based on held modifiers (Shift/Alt) */
export function stepFromModifiers() {
  if (keysDown.has("shift")) return CONST.STEP_COARSE;
  if (keysDown.has("alt"))   return CONST.STEP_FINE;
  return CONST.STEP_BASE;
}

/* Switch active view (used in 4D) */
export function setActiveView(v) {
  state.activeView = (v === "B") ? "B" : "A";
}

/* =========================================================
   Axis helpers
   ========================================================= */
export function buildAxisNames(dim) {
  const names = ["x", "y", "z", "w"];
  state.axisNames = names.slice(0, Math.max(0, Math.min(4, dim|0)));
  return state.axisNames;
}

/* =========================================================
   Normalisation helpers (0..1) ↔︎ (-1..1)
   These are the ONLY source of truth for mapping.
   ========================================================= */

/** u∈[-1,1] → value in [boundsMin[j], boundsMax[j]] (usually [0,1]) */
export function uToLatent(u, j, boundsMin = state.boundsMin, boundsMax = state.boundsMax) {
  const lo = boundsMin?.[j]; const hi = boundsMax?.[j];
  if (!isFinite(lo) || !isFinite(hi) || hi === lo) return 0.0;
  const t = (clamp(u, -1, 1) + 1) * 0.5;          // [-1,1] → [0,1]
  return lo + t * (hi - lo);
}

/** value in [boundsMin[j], boundsMax[j]] → u∈[-1,1] */
export function latentToU(v, j, boundsMin = state.boundsMin, boundsMax = state.boundsMax) {
  const lo = boundsMin?.[j]; const hi = boundsMax?.[j];
  if (!isFinite(lo) || !isFinite(hi) || hi === lo) return 0.0;
  const t = (v - lo) / (hi - lo);                 // → [0,1]
  return clamp(t * 2 - 1, -1, 1);                 // → [-1,1]
}

/* =========================================================
   Generic utilities
   ========================================================= */
export function clamp(x, lo, hi) {
  return Math.min(hi, Math.max(lo, x));
}
export function lerp(a, b, t) {
  return a + (b - a) * t;
}

/** Read a CSS custom property as string (no fallback here) */
export function cssVar(name) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(name).trim();
}
/** Convenience for numeric CSS vars */
export function cssNumber(name) {
  const v = parseFloat(cssVar(name));
  return Number.isFinite(v) ? v : undefined;
}

/* =========================================================
   Small helpers for arrays/vectors
   ========================================================= */
export function vecFill(n, value = 0) {
  return Array.from({ length: n }, () => value);
}
export function vecLerp(dst, src, alpha) {
  const n = Math.min(dst.length, src.length);
  for (let i = 0; i < n; i++) dst[i] = lerp(dst[i], src[i], alpha);
  return dst;
}

/* =========================================================
   DOM helpers for selects (optional, used in ui.js)
   ========================================================= */

/** Populate a <select> with [{value,label}] options. Keeps current selection if possible. */
export function populateSelect(selectEl, options, placeholder) {
  if (!selectEl) return;
  const prev = selectEl.value;
  selectEl.innerHTML = "";
  if (placeholder) {
    const ph = document.createElement("option");
    ph.value = ""; ph.textContent = placeholder;
    selectEl.appendChild(ph);
  }
  for (const { value, label } of options) {
    const opt = document.createElement("option");
    opt.value = String(value);
    opt.textContent = String(label);
    selectEl.appendChild(opt);
  }
  if (prev && [...selectEl.options].some(o => o.value === prev)) {
    selectEl.value = prev;
  }
}

/* =========================================================
   Convenience: compute bounds from latent (safety)
   ========================================================= */
export function recomputeBoundsFromLatent() {
  if (!Array.isArray(state.latent) || state.latent.length === 0) return;
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

/* =========================================================
   Keyboard helpers (attach/detach once, used in main.js)
   ========================================================= */
export function attachKeyListeners() {
  window.addEventListener("keydown", handleKeyDown, { passive: false });
  window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
}
export function detachKeyListeners() {
  window.removeEventListener("keydown", handleKeyDown);
  window.removeEventListener("keyup",   handleKeyUp);
}
function handleKeyDown(e) {
  const k = normaliseKey(e.key);
  keysDown.add(k);
  // prevent arrow-like behaviour only for our keys
  if (["a","d","w","s","f","h","t","g","q","e"].includes(k)) {
    e.preventDefault();
  }
}
function handleKeyUp(e) {
  keysDown.delete(normaliseKey(e.key));
}
function normaliseKey(k) {
  k = (k || "").toLowerCase();
  if (k === "shift") return "shift";
  if (k === "alt" || k === "altgraph") return "alt";
  return k.length === 1 ? k : k;
}
