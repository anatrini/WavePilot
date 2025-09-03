// main.js
/* global Plotly */
import {
  state, CONST, clamp, currentStep, buildAxisNames,
  latentToU, uToLatent, populateSelect
} from "./core.js";
import { /* usiamo solo gli ID in HTML per i plot; il resto della UI resta com'è */ } from "./ui.js";
import { drawPlots, updateCursor } from "./plot.js";    // drawPlots gestisce single o dual automaticamente
import { sendCursor, setupSocket } from "./net.js";

// ---- Gestione tastiera su vista attiva (A o B) ----
let activeView = "A"; // "A" o "B" in modalità 4D dual; ignorato in 2D/3D

// Stato tastiera per movimenti simultanei
const keysDown = new Set();
const modifiers = { shift: false, alt: false };

// function applyKeyToView(u, viewAxes, step, key) {
//   // X (←/→ o A/D)
//   if (key === "ArrowLeft" || key === "a" || key === "A") {
//     u[viewAxes.x] = clamp(u[viewAxes.x] - step, -1, 1); return true;
//   } else if (key === "ArrowRight" || key === "d" || key === "D") {
//     u[viewAxes.x] = clamp(u[viewAxes.x] + step, -1, 1); return true;
//   }
//   // Y (↑/↓ o W/S)
//   if (key === "ArrowUp" || key === "w" || key === "W") {
//     u[viewAxes.y] = clamp(u[viewAxes.y] + step, -1, 1); return true;
//   } else if (key === "ArrowDown" || key === "s" || key === "S") {
//     u[viewAxes.y] = clamp(u[viewAxes.y] - step, -1, 1); return true;
//   }
//   return false;
// }

function handleKeyDown(e) {
  if (state.inputSource !== "keyboard") return;
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
  if (tag === "input" || tag === "select" || tag === "textarea") return;

  const k = (e.key || "").toLowerCase();
  // tasti che gestiamo: A D W S (sinistra), F H T G (destra), più Shift/Alt per lo step
  if (["a","d","w","s","f","h","t","g","shift","alt"].includes(k)) {
    e.preventDefault();
    keysDown.add(k);
    if (k === "shift") modifiers.shift = true;
    if (k === "alt")   modifiers.alt   = true;
  }
}

function handleKeyUp(e) {
  const k = (e.key || "").toLowerCase();
  keysDown.delete(k);
  if (k === "shift") modifiers.shift = false;
  if (k === "alt")   modifiers.alt   = false;
}


function stepFromModifiers() {
  if (modifiers.shift) return CONST.STEP_COARSE;
  if (modifiers.alt)   return CONST.STEP_FINE;
  return CONST.STEP_BASE;
}

function applyKeyboardInput() {
  if (keysDown.size === 0) return;

  const step = stepFromModifiers();
  const u = state.uTarget.slice(); // accumula partendo dal target corrente

  const add = (idx, delta) => {
    if (typeof idx === "number" && Number.isFinite(idx)) {
      u[idx] = clamp(u[idx] + delta, -1, 1);
    }
  };

  if (state.dim === 4) {
    // Vista SINISTRA: A/D (X), W/S (Y)
    const a = state.currentAxesA || { x: 0, y: 1 };
    if (keysDown.has("a")) add(a.x, -step);
    if (keysDown.has("d")) add(a.x,  step);
    if (keysDown.has("w")) add(a.y,  step);
    if (keysDown.has("s")) add(a.y, -step);

    // Vista DESTRA: F/H (X), T/G (Y)
    const b = state.currentAxesB || { x: 2, y: 3 };
    if (keysDown.has("f")) add(b.x, -step);
    if (keysDown.has("h")) add(b.x,  step);
    if (keysDown.has("t")) add(b.y,  step);
    if (keysDown.has("g")) add(b.y, -step);
  } else {
    // 2D/3D → come la vista sinistra: A/D (X), W/S (Y)
    const ax = Number(state.currentAxes.x);
    const ay = Number(state.currentAxes.y);
    if (keysDown.has("a")) add(ax, -step);
    if (keysDown.has("d")) add(ax,  step);
    if (keysDown.has("w")) add(ay,  step);
    if (keysDown.has("s")) add(ay, -step);
  }

  state.uTarget = u;
}



// ---- Loop di smoothing + invio cursor ----
function tickSmooth() {
  applyKeyboardInput();
  let moved = false;
  for (let i = 0; i < state.dim; i++) {
    const prev = state.uCurrent[i];
    const next = prev + CONST.LERP_ALPHA * (state.uTarget[i] - prev);
    if (Math.abs(next - prev) > CONST.MOVE_EPS) moved = true;
    state.uCurrent[i] = next;
  }

  if (moved) {
    const lp = state.uCurrent.map((uu, j) => uToLatent(uu, j));
    state.cursorPoint = lp;
    updateCursor(lp);  // aggiorna la/le viste (single o dual)

    const now = (typeof performance !== "undefined" ? performance.now() : Date.now());
    if (now - state.lastSendTs >= CONST.SEND_INTERVAL_MS) {
      sendCursor(lp);
      state.lastSendTs = now;
    }
  }
  requestAnimationFrame(tickSmooth);
}

// ---- Setup controlli dual per 4D ----
function setupDual2DControls() {
  const selAX = document.getElementById("axis-a-x");
  const selAY = document.getElementById("axis-a-y");
  const selBX = document.getElementById("axis-b-x");
  const selBY = document.getElementById("axis-b-y");

  // default: (0,1) a sinistra, (2,3) a destra
  state.currentAxesA = state.currentAxesA || { x: 0, y: 1 };
  state.currentAxesB = state.currentAxesB || { x: 2, y: 3 };

  populateSelect(selAX, state.dim, state.currentAxesA.x, state.axisNames);
  populateSelect(selAY, state.dim, state.currentAxesA.y, state.axisNames);
  populateSelect(selBX, state.dim, state.currentAxesB.x, state.axisNames);
  populateSelect(selBY, state.dim, state.currentAxesB.y, state.axisNames);

  const onChangeA = () => {
    state.currentAxesA.x = Number(selAX.value);
    state.currentAxesA.y = Number(selAY.value);
    drawPlots(); if (state.cursorPoint) updateCursor(state.cursorPoint);
  };
  const onChangeB = () => {
    state.currentAxesB.x = Number(selBX.value);
    state.currentAxesB.y = Number(selBY.value);
    drawPlots(); if (state.cursorPoint) updateCursor(state.cursorPoint);
  };

  selAX.addEventListener("change", onChangeA);
  selAY.addEventListener("change", onChangeA);
  selBX.addEventListener("change", onChangeB);
  selBY.addEventListener("change", onChangeB);

  // Attiva focus tastiera per la vista cliccata
  const plotLeft = document.getElementById("plot-left");
  const plotRight = document.getElementById("plot-right");
  if (plotLeft && typeof plotLeft.on === "function") {
    plotLeft.on("plotly_click", (ev) => {
      activeView = "A";
      handlePlotClick(ev, state.currentAxesA);
    });
  }
  if (plotRight && typeof plotRight.on === "function") {
    plotRight.on("plotly_click", (ev) => {
      activeView = "B";
      handlePlotClick(ev, state.currentAxesB);
    });
  }
}

// Click su una vista: aggiorna solo le 2 dimensioni mappate in quella vista
function handlePlotClick(ev, viewAxes) {
  if (state.inputSource !== "mouse") return;
  if (!ev || !ev.points || !ev.points.length) return;

  const p = ev.points[0];
  const lp = state.cursorPoint ? state.cursorPoint.slice() : new Array(state.dim).fill(0);
  lp[viewAxes.x] = uToLatent(p.x, viewAxes.x);
  lp[viewAxes.y] = uToLatent(p.y, viewAxes.y);

  // le altre dimensioni restano dove sono (cursorPoint attuale)
  const u = lp.map((val, j) => latentToU(val, j));
  state.uTarget = u.map(v => clamp(v, -1, 1));
}

// ---- Boot ----
(async function init() {
  // 1) Carica dati/meta
  const resp = await fetch("/data");
  const meta = await resp.json();
  state.latent = meta.latent;
  state.dim = meta.dim;
  state.boundsMin = meta.bounds_min;
  state.boundsMax = meta.bounds_max;

   // Ricalcola bounds dai dati (sicuro: 0..1 nel tuo caso)
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

  // 2) Inizializza u/cursor
  state.uCurrent = new Array(state.dim).fill(0.0);
  state.uTarget  = new Array(state.dim).fill(0.0);
  state.cursorPoint = state.uCurrent.map((uu, j) => uToLatent(uu, j));

  // 3) Inizializza controlli sorgente input
  const selInput = document.getElementById("input-source");
  state.inputSource = (selInput && selInput.value) ? selInput.value : "keyboard";
  if (selInput) {
    selInput.addEventListener("change", () => {
      state.inputSource = selInput.value; // "keyboard" | "mouse" | "osc"
      if (state.inputSource === "keyboard") {
        window.addEventListener("keydown", handleKeyDown, { passive: false });
        window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
      } else {
        window.removeEventListener("keydown", handleKeyDown);
        window.removeEventListener("keyup",   handleKeyUp);
      }
    });
  }


  // 4) Point selector (identico)
  const selPoint = document.getElementById("point-select");
  if (selPoint) {
    selPoint.innerHTML = '<option value="">— select point —</option>';
    for (let i = 0; i < state.latent.length; i++) {
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = `Point ${i}`;
      selPoint.appendChild(opt);
    }
    selPoint.addEventListener("change", () => {
      const v = selPoint.value;
      if (v === "") return;
      const idx = Number(v);
      if (!Number.isFinite(idx) || idx < 0 || idx >= state.latent.length) return;
      state.cursorPoint = state.latent[idx].slice();
      updateCursor(state.cursorPoint);
      sendCursor(state.cursorPoint);
    });
  }

  // 5) Mostra/nascondi controlli in base alla dimensionalità
  const singleAxisControls = document.getElementById("single-axis-controls"); // X/Y[/Z] legacy
  const dualAxisControls   = document.getElementById("dual-axis-controls");   // A/B (nuovi)

  if (state.dim <= 3) {
    // 2D/3D → UI invariata
    if (singleAxisControls) singleAxisControls.style.display = "";
    if (dualAxisControls)   dualAxisControls.style.display   = "none";
  } else {
    // 4D → dual 2D, via A/B
    if (singleAxisControls) singleAxisControls.style.display = "none";
    if (dualAxisControls)   dualAxisControls.style.display   = "flex";
  }

  // 6) Disegno iniziale
  drawPlots();                   // gestisce single vs dual internamente
  updateCursor(state.cursorPoint);

  // 7) Wiring specifico per 4D dual
  if (state.dim === 4) {
    setupDual2DControls();

    // Memorizza la vista attiva sul click dei contenitori (per tastiera)
    const leftEl  = document.getElementById("plot-left");
    const rightEl = document.getElementById("plot-right");
    if (leftEl)  leftEl.addEventListener("click", () => { activeView = "A"; });
    if (rightEl) rightEl.addEventListener("click", () => { activeView = "B"; });
  }

  // 8) Loop di smoothing
  requestAnimationFrame(tickSmooth);

  // 9) Attiva listeners tastiera se serve
  if (state.inputSource === "keyboard") {
    window.addEventListener("keydown", handleKeyDown, { passive: false });
    window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
  }

  // 10) Socket → aggiorna cursor e viste
  setupSocket((lp) => {
    state.cursorPoint = lp;
    updateCursor(lp);
  });
})();
