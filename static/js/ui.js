// ui.js
// DOM queries and UI helpers for both classic (2D/3D) and dual-2D (4D) modes.

import { state, populateSelect, updateControlsVisibility } from "./core.js";

export const dom = {
  // CLASSIC (2D/3D)
  //plotEl: document.getElementById("plot-container"),
  selInput: document.getElementById("input-source"),
  selPoint: document.getElementById("preset-select"),
  selX: document.getElementById("axis-x"),
  selY: document.getElementById("axis-y"),
  selZ: document.getElementById("axis-z"),

  // DUAL-2D (4D)
  plotLeft: document.getElementById("plot-container-left"),
  plotRight: document.getElementById("plot-container-right"),
  pairControls: document.getElementById("pair-controls"),
  selA1: document.getElementById("axis-a1"),
  selA2: document.getElementById("axis-a2"),
  selB1: document.getElementById("axis-b1"),
  selB2: document.getElementById("axis-b2"),
  classicControls: document.getElementById("classic-controls"),
};

export function enableDual2DUI() {
  // nascondi Z e vecchi slice/w
  if (dom.classicControls) dom.classicControls.style.display = "none";
  //if (dom.wControls) dom.wControls.style.display = "none";
  const zEls = document.querySelectorAll(".z-only, #axis-z");
  zEls.forEach(e => e.style.display = "none");

  // mostra doppia vista
  if (dom.pairControls) dom.pairControls.style.display = "grid";
  const wrapper = document.getElementById("plot-wrapper");
  if (wrapper) wrapper.classList.add("dual");
  //if (dom.plotEl) dom.plotEl.style.display = "none";
  if (dom.plotLeft) dom.plotLeft.style.display = "block";
  if (dom.plotRight) dom.plotRight.style.display = "block";
}

export function enableClassicUI() {
  if (dom.classicControls) dom.classicControls.style.display = "";
  const zEls = document.querySelectorAll(".z-only, #axis-z");
  zEls.forEach(e => e.style.display = "");
  //if (dom.wControls) dom.wControls.style.display = "none"; // niente slice in nuova organizzazione

  if (dom.pairControls) dom.pairControls.style.display = "none";
  const wrapper = document.getElementById("plot-wrapper");
  if (wrapper) wrapper.classList.remove("dual");
  //if (dom.plotEl) dom.plotEl.style.display = "block";
  if (dom.plotLeft) dom.plotLeft.style.display = "none";
  if (dom.plotRight) dom.plotRight.style.display = "none";
}

export function syncAxisSelectors(drawPlot, updateCursor) {
  // Per 2D/3D rimane identico
  const { selX, selY, selZ } = dom;
  const n = state.dim, labels = state.axisNames;

  populateSelect(selX, n, 0, labels);
  populateSelect(selY, n, 1, labels);
  if (n >= 3) populateSelect(selZ, n, Math.min(2, n - 1), labels);

  updateControlsVisibility(state.dim);

  selX.addEventListener("change", () => {
    state.currentAxes.x = Number(selX.value);
    drawPlot();
    if (state.cursorPoint) updateCursor(state.cursorPoint);
  });

  selY.addEventListener("change", () => {
    state.currentAxes.y = Number(selY.value);
    drawPlot();
    if (state.cursorPoint) updateCursor(state.cursorPoint);
  });

  selZ.addEventListener("change", () => {
    state.currentAxes.z = Number(selZ.value);
    drawPlot();
    if (state.cursorPoint) updateCursor(state.cursorPoint);
  });
}

export function syncAxisPairSelectors(drawPlot, updateCursor) {
  const { selA1, selA2, selB1, selB2 } = dom;
  const n = state.dim, labels = state.axisNames;

  // popolamento iniziale
  populateSelect(selA1, n, state.viewA.i, labels);
  populateSelect(selA2, n, state.viewA.j, labels);
  populateSelect(selB1, n, state.viewB.i, labels);
  populateSelect(selB2, n, state.viewB.j, labels);

  const onChange = () => {
    state.viewA.i = Number(selA1.value);
    state.viewA.j = Number(selA2.value);
    state.viewB.i = Number(selB1.value);
    state.viewB.j = Number(selB2.value);
    drawPlot();
    if (state.cursorPoint) updateCursor(state.cursorPoint);
  };

  selA1.addEventListener("change", onChange);
  selA2.addEventListener("change", onChange);
  selB1.addEventListener("change", onChange);
  selB2.addEventListener("change", onChange);
}
