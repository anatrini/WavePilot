// -------------------------------------------------------
// UI wiring & helpers
// -------------------------------------------------------
import { state } from "./core.js";
import { drawPlots, updateCursor } from "./plot.js";

// Espongo tutti i riferimenti che usiamo altrove
export const UI = {
  // fieldset "Input"
  selInput:      document.getElementById("input-source"),

  // fieldset "Presets"
  selPreset:     document.getElementById("preset-select"),

  // fieldset "Axes (2D/3D)"
  selX:          document.getElementById("axis-x"),
  selY:          document.getElementById("axis-y"),
  selZ:          document.getElementById("axis-z"),

  // fieldset "View A / View B" (4D)
  selAX:         document.getElementById("axis-a-x"),
  selAY:         document.getElementById("axis-a-y"),
  selBX:         document.getElementById("axis-b-x"),
  selBY:         document.getElementById("axis-b-y"),

  // pannello shortcuts
  shortcuts:     document.getElementById("shortcuts"),

  // gruppi per mostra/nascondi
  singleGroup:   document.getElementById("single-axis-controls"),
  dualGroup:     document.getElementById("dual-axis-controls"),
};

// -------------------------------------------------------
// Axis labels & select population
// -------------------------------------------------------
export function buildAxisNames(dim) {
  // x, y, z, w (tag coerenti con il resto degli strumenti)
  state.axisNames = ["x", "y", "z", "w"].slice(0, Math.max(2, Math.min(4, dim)));
}

function populateSelect(sel, labels, defaultIdx = 0) {
  if (!sel) return;
  sel.innerHTML = "";
  labels.forEach((lab, i) => {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = lab;
    sel.appendChild(opt);
  });
  sel.value = String(defaultIdx);
}

/**
 * 2D/3D: prepara i menu a tendina per X/Y[/Z] e collega i listener.
 * Ridisegna i plot quando cambia una selezione.
 */
export function setupAxisSelectors() {
  if (!state.axisNames || state.axisNames.length < 2) return;

  // default axes
  if (!state.currentAxes) state.currentAxes = { x: 0, y: 1, z: Math.min(2, state.dim - 1) };

  // Popola i select
  populateSelect(UI.selX, state.axisNames, state.currentAxes.x);
  populateSelect(UI.selY, state.axisNames, state.currentAxes.y);

  // Z solo in 3D
  if (state.dim === 3 && UI.selZ) {
    UI.selZ.parentElement?.classList?.remove("z-only"); // assicurati visibile
    populateSelect(UI.selZ, state.axisNames, state.currentAxes.z);
  } else if (UI.selZ) {
    UI.selZ.parentElement?.classList?.add("z-only"); // resta nascosto in 2D/4D
  }

  // Listener
  if (UI.selX) UI.selX.onchange = () => {
    state.currentAxes.x = Number(UI.selX.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
  if (UI.selY) UI.selY.onchange = () => {
    state.currentAxes.y = Number(UI.selY.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
  if (state.dim === 3 && UI.selZ) UI.selZ.onchange = () => {
    state.currentAxes.z = Number(UI.selZ.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
}

/**
 * 4D: due viste 2D indipendenti, con X/Y per View A e X/Y per View B.
 */
export function setupDual2DControls() {
  if (state.dim !== 4) return;

  // default axes per viste A e B
  if (!state.currentAxesA) state.currentAxesA = { x: 0, y: 1 };
  if (!state.currentAxesB) state.currentAxesB = { x: 2, y: 3 };

  // Popola i select per entrambe le viste
  populateSelect(UI.selAX, state.axisNames, state.currentAxesA.x);
  populateSelect(UI.selAY, state.axisNames, state.currentAxesA.y);
  populateSelect(UI.selBX, state.axisNames, state.currentAxesB.x);
  populateSelect(UI.selBY, state.axisNames, state.currentAxesB.y);

  // Listener → aggiorna lo stato e ridisegna
  if (UI.selAX) UI.selAX.onchange = () => {
    state.currentAxesA.x = Number(UI.selAX.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
  if (UI.selAY) UI.selAY.onchange = () => {
    state.currentAxesA.y = Number(UI.selAY.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
  if (UI.selBX) UI.selBX.onchange = () => {
    state.currentAxesB.x = Number(UI.selBX.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
  if (UI.selBY) UI.selBY.onchange = () => {
    state.currentAxesB.y = Number(UI.selBY.value);
    drawPlots(); updateCursor(state.cursorPoint);
  };
}

// -------------------------------------------------------
// Shortcuts: show/hide per input mode e dimensionalità
// -------------------------------------------------------
export function refreshShortcuts() {
  if (!UI.shortcuts) return;
  UI.shortcuts.dataset.mode = state.inputSource || "keyboard"; // keyboard | mouse | osc
  UI.shortcuts.dataset.dim  = String(state.dim || 2);          // "2" | "3" | "4"
}

// -------------------------------------------------------
// Keyboard helpers (richiesti da main.js anche se opzionali)
// -------------------------------------------------------
export function attachKeyListeners(onDown, onUp) {
  if (typeof onDown === "function") {
    window.addEventListener("keydown", onDown, { passive: false });
  }
  if (typeof onUp === "function") {
    window.addEventListener("keyup", onUp, { passive: true });
  }
}
export function detachKeyListeners(onDown, onUp) {
  if (typeof onDown === "function") {
    window.removeEventListener("keydown", onDown);
  }
  if (typeof onUp === "function") {
    window.removeEventListener("keyup", onUp);
  }
}
