// -------------------------------------------------------
// Main orchestrator
// -------------------------------------------------------
import { state, uToLatent, clamp, CONST } from './core.js';
import { UI, buildAxisNames, setupAxisSelectors, setupDual2DControls,
         refreshShortcuts, attachKeyListeners, detachKeyListeners } from './ui.js';
import { drawPlots, updateCursor } from './plot.js';
import { setupSocket, sendCursor } from './net.js';

// Keyboard state
const keysDown = new Set();

// --- helpers ---
function stepFromModifiers(ev) {
  // use movement constants from core.js
  if (ev?.altKey)   return CONST.STEP_FINE;
  if (ev?.shiftKey) return CONST.STEP_COARSE;
  return CONST.STEP_BASE;
}

// Resize plots when window changes
function resizePlots() {
  const left = document.getElementById('plot-left');
  if (left && left.offsetParent !== null) Plotly.Plots.resize(left);
  const right = document.getElementById('plot-right');
  if (state.dim === 4 && right && right.offsetParent !== null) Plotly.Plots.resize(right);
}

// Apply keyboard input to uTarget (2D / 3D / 4D)
function applyKeyboardInput() {
  if (keysDown.size === 0) return;

  const step = (keysDown.has('alt') ? CONST.STEP_FINE :
               keysDown.has('shift') ? CONST.STEP_COARSE : CONST.STEP_BASE);

  const u = state.uTarget.slice();
  const add = (idx, delta) => {
    if (typeof idx === 'number' && Number.isFinite(idx)) {
      u[idx] = clamp(u[idx] + delta, -1, 1);
    }
  };

  if (state.dim === 4) {
    const a = state.currentAxesA || { x: 0, y: 1 };
    const b = state.currentAxesB || { x: 2, y: 3 };
    if (keysDown.has('a')) add(a.x, -step);
    if (keysDown.has('d')) add(a.x,  step);
    if (keysDown.has('w')) add(a.y,  step);
    if (keysDown.has('s')) add(a.y, -step);
    if (keysDown.has('f')) add(b.x, -step);
    if (keysDown.has('h')) add(b.x,  step);
    if (keysDown.has('t')) add(b.y,  step);
    if (keysDown.has('g')) add(b.y, -step);
  } else {
    const ax = Number(state.currentAxes.x);
    const ay = Number(state.currentAxes.y);
    // XY
    if (keysDown.has('a')) add(ax, -step);
    if (keysDown.has('d')) add(ax,  step);
    if (keysDown.has('w')) add(ay,  step);
    if (keysDown.has('s')) add(ay, -step);
    // Z in 3D
    if (state.dim === 3) {
      const az = Number(state.currentAxes.z);
      if (keysDown.has('q')) add(az,  step);
      if (keysDown.has('e')) add(az, -step);
    }
  }

  state.uTarget = u;
}

// Key handlers
function handleKeyDown(ev) {
  const k = (ev.key || '').toLowerCase();
  const allowedKeys = ['a','d','w','s','q','e','f','h','t','g','shift','alt'];
  if (!allowedKeys.includes(k)) return;
  ev.preventDefault();
  keysDown.add(k);
}
function handleKeyUp(ev) {
  const k = (ev.key || '').toLowerCase();
  keysDown.delete(k);
}

// Smoothing loop
function tickSmooth() {
  // Accept keyboard input
  if (state.inputSource === 'keyboard') applyKeyboardInput();

  // Lerp on uCurrent
  const alpha = CONST.LERP_ALPHA;
  let moved = false;
  for (let i = 0; i < state.dim; i++) {
    const prev = state.uCurrent[i];
    const next = prev + (state.uTarget[i] - prev) * alpha;
    state.uCurrent[i] = next;
    if (Math.abs(next - prev) > CONST.MOVE_EPS) moved = true;
  }

  if (moved) {
    // Denormalise to [0,1] and update plot
    const latentPoint = state.uCurrent.map((uu, j) => uToLatent(uu, j));
    state.cursorPoint = latentPoint;
    updateCursor(latentPoint);
    sendCursor(latentPoint);
  }
  requestAnimationFrame(tickSmooth);
}

// -------------------------------------------------------
// Boot
// -------------------------------------------------------
(async function init() {
  // 1) Load data/meta
  const resp = await fetch('/data');
  const meta = await resp.json();

  state.latent    = meta.latent;
  state.dim       = meta.dim;
  state.boundsMin = meta.bounds_min;
  state.boundsMax = meta.bounds_max;

  // Preset names: from server or fallback ID1..N
  const N = state.latent.length;
  if (Array.isArray(meta.preset_names) && meta.preset_names.length === N) {
    state.presetNames = meta.preset_names.map(s => (s == null || s === '') ? null : String(s));
  } else {
    state.presetNames = new Array(N).fill(null);
  }
  for (let i = 0; i < N; i++) if (!state.presetNames[i]) state.presetNames[i] = `ID${i+1}`;

  // Recalculate bounds (safe: 0..1 in your case)
  if (Array.isArray(state.latent) && state.latent.length > 0) {
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

  buildAxisNames(state.dim);
  setupAxisSelectors();
  refreshShortcuts(); // show the correct blocks for 2D/3D/4D

  // 2) Initialise u/cursor
  state.uCurrent = new Array(state.dim).fill(0.0);
  state.uTarget  = new Array(state.dim).fill(0.0);
  state.cursorPoint = state.uCurrent.map((uu, j) => uToLatent(uu, j));

  // 3) Input source
  if (UI.selInput) {
    state.inputSource = UI.selInput.value || 'keyboard';
    if (state.inputSource === 'keyboard') {
      window.addEventListener('keydown', handleKeyDown, { passive: false });
      window.addEventListener('keyup',   handleKeyUp,   { passive: true  });
    }
    UI.selInput.addEventListener('change', () => {
      state.inputSource = UI.selInput.value;
      if (state.inputSource === 'keyboard') {
        window.addEventListener('keydown', handleKeyDown, { passive: false });
        window.addEventListener('keyup',   handleKeyUp,   { passive: true  });
      } else {
        window.removeEventListener('keydown', handleKeyDown);
        window.removeEventListener('keyup',   handleKeyUp);
        keysDown.clear();
      }
      refreshShortcuts();
    });
  }

  // 4) Preset selector
  const selPoint = document.getElementById('preset-select');
  if (selPoint) {
    selPoint.innerHTML = '<option value="">— select preset —</option>';
    for (let i = 0; i < state.presetNames.length; i++) {
      const opt = document.createElement('option');
      opt.value = String(i);
      opt.textContent = state.presetNames[i];
      selPoint.appendChild(opt);
    }
    selPoint.addEventListener('change', () => {
      const v = selPoint.value;
      if (v === '') return;
      const idx = Number(v);
      if (!Number.isFinite(idx) || idx < 0 || idx >= state.latent.length) return;
      state.cursorPoint = state.latent[idx].slice();   // [0,1]
      updateCursor(state.cursorPoint);
      sendCursor(state.cursorPoint);
    });
  }

  // 5) Show/hide controls for 2D/3D/4D
  const singleAxisControls = document.getElementById('single-axis-controls');
  const dualAxisControls   = document.getElementById('dual-axis-controls');
  if (state.dim <= 3) {
    if (singleAxisControls) singleAxisControls.style.display = '';
    if (dualAxisControls)   dualAxisControls.style.display   = 'none';
  } else {
    if (singleAxisControls) singleAxisControls.style.display = 'none';
    if (dualAxisControls)   dualAxisControls.style.display   = 'flex';
  }

  // 6) Initial drawing
  drawPlots();
  updateCursor(state.cursorPoint);
  // Initial resize + resize on window
  resizePlots();
  window.addEventListener('resize', resizePlots, { passive: true });

  // 7) Specific wiring for 4D dual
  if (state.dim === 4) {
    setupDual2DControls();
    const leftEl  = document.getElementById('plot-left');
    const rightEl = document.getElementById('plot-right');
    if (leftEl)  leftEl.addEventListener('click', () => { state.activeView = 'A'; });
    if (rightEl) rightEl.addEventListener('click', () => { state.activeView = 'B'; });
  }

  // 8) Loop smoothing
  requestAnimationFrame(tickSmooth);

  // 9) Socket → update cursor and views
  setupSocket((lp) => {
    state.cursorPoint = lp;
    updateCursor(lp);
  });
})();
