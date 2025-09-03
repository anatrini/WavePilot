// ui.js
// DOM queries and small UI helpers.

import { state, populateSelect, updateControlsVisibility } from "./core.js";

export const dom = {
  plotEl: document.getElementById("plot-container"),
  selInput: document.getElementById("input-source"),
  selPoint: document.getElementById("point-select"),
  selX: document.getElementById("axis-x"),
  selY: document.getElementById("axis-y"),
  selZ: document.getElementById("axis-z"),
  wControls: document.getElementById("slice-controls"),
  wSlider: document.getElementById("w-slider"),
  wReadout: document.getElementById("w-value"),
};

export function syncAxisSelectors(drawPlot, updateCursor) {
  const { selX, selY, selZ, wControls } = dom;
  const n = state.dim, labels = state.axisNames;

  populateSelect(selX, n, 0, labels);
  populateSelect(selY, n, 1, labels);
  if (n >= 3) populateSelect(selZ, n, Math.min(2, n - 1), labels);

  updateControlsVisibility(state.dim, wControls);

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
