// core.js
// Central state, constants, and helpers used across modules.

export const CONST = {
  CURSOR_GLOW_SIZE: 18,
  CURSOR_GLOW_COLOR: "rgb(255,200,120)",
  CURSOR_GLOW_OPACITY: 0.25,
  CURSOR_DOT_SIZE: 7,
  CURSOR_DOT_COLOR: "rgb(255,210,150)",
  CURSOR_DOT_LINE: "#ffffff",
  MARKER_COLOR: "#6ea8fe",
  BG_COLOR: "#101214",
  STEP_BASE: 0.03,
  STEP_FINE: 0.01,
  STEP_COARSE: 0.1,
  LERP_ALPHA: 0.25,
  SEND_INTERVAL_MS: 60,
  MOVE_EPS: 1e-3,
};

export const state = {
  latent: [],             // NxD
  dim: 0,                 // D
  boundsMin: [],
  boundsMax: [],
  axisNames: [],          // ["z0","z1","z2","z3"]
  // Vista "classica" (2D/3D)
  currentAxes: { x: 0, y: 1, z: 2 },
  is3D: false,

  // Nuove viste duali per 4D
  viewA: { i: 0, j: 1 },  // default: (z0,z1)
  viewB: { i: 2, j: 3 },  // default: (z2,z3)
  cursorTraces: {
    A: { glow: -1, dot: -1 },
    B: { glow: -1, dot: -1 },
  },

  inputSource: "keyboard", // "osc" | "mouse" | "keyboard"
  cursorPoint: null,      // array length D
  uCurrent: [],
  uTarget: [],
  lastSendTs: 0,

  // Campi legacy slice (non più usati in 4D, tenuti per compat. 2D/3D)
  sliceW0: null,
  sliceDim: null,
  wValue: 0.0,

  keyNavEnabled: false,
  localSeq: 0,
  lastAppliedSeq: -1,
  cursorGlowIdx: -1,
  cursorDotIdx: -1,
  lastCamera: null,
};

export function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
export const clamp11 = v => clamp(v, -1, 1);
// NOTE: kept identical semantics to the original file (compat).
export function clamp01(x) { return Math.min(1, Math.max(-1, x)); }

export function currentStep(e) {
  if (e && e.shiftKey) return CONST.STEP_COARSE;
  if (e && e.altKey) return CONST.STEP_FINE;
  return CONST.STEP_BASE;
}

export function populateSelect(el, n, selectedIdx = 0, labels = null) {
  el.innerHTML = "";
  for (let i = 0; i < n; i++) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = labels ? labels[i] : "z" + i;
    if (i === selectedIdx) opt.selected = true;
    el.appendChild(opt);
  }
}

export function updateControlsVisibility(dim, wControlsEl) {
  const zEls = document.querySelectorAll(".z-only, #axis-z");
  if (dim === 2) {
    zEls.forEach(e => e.style.display = "none");
  } else {
    zEls.forEach(e => e.style.display = "");
  }
  if (wControlsEl) wControlsEl.style.display = (dim === 4 ? "none" : "none"); // sempre nascosto in nuova 4D
}

export function buildAxisNames(n) {
  state.axisNames = Array.from({ length: n }, (_, i) => "z" + i);
}

export const getColumn = (arr, idx) => arr.map(row => row[idx]);

// Map latent coordinate -> normalised cursor u in [-1,1]
export function latentToU(val, dimIdx) {
  const lo = state.boundsMin[dimIdx], hi = state.boundsMax[dimIdx];
  const denom = Math.max(1e-12, (hi - lo));
  const u = 2.0 * (val - lo) / denom - 1.0;
  return clamp(u, -1.0, 1.0);
}

// Map normalised cursor u in [-1,1] -> latent coordinate
export function uToLatent(u, dimIdx) {
  const uu = Math.max(-1, Math.min(1, Number.isFinite(u) ? u : 0));
  const lo = state.boundsMin[dimIdx], hi = state.boundsMax[dimIdx];
  const span = Math.max(1e-12, (hi - lo));
  return (uu + 1.0) * 0.5 * span + lo;
}
