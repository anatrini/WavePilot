// ui.js — controlli sidebar, shortcuts e selettori assi

import { state } from "./core.js";
import { drawPlots, updateCursor } from "./plot.js";

/* ----------
   DOM cache
   ---------- */
export const dom = {
  selInput: document.getElementById("input-source"),
  selPoint: document.getElementById("preset-select"),

  // 2D/3D
  selX: document.getElementById("axis-x"),
  selY: document.getElementById("axis-y"),
  selZ: document.getElementById("axis-z"),

  // 4D (dual 2D views)
  selAX: document.getElementById("axis-a-x"),
  selAY: document.getElementById("axis-a-y"),
  selBX: document.getElementById("axis-b-x"),
  selBY: document.getElementById("axis-b-y"),

  // groups
  singleAxisControls: document.getElementById("single-axis-controls"),
  dualAxisControls:   document.getElementById("dual-axis-controls"),

  // shortcuts panel
  shortcutsFS: document.getElementById("shortcuts"),
};

/* ----------------------
   Helpers (UI utilities)
   ---------------------- */
const AX_LABELS = ["x", "y", "z", "w"];
const axLabel = (i) => AX_LABELS[i] ?? `z${i}`;

function optionList(dim){
  const n = Number(dim) || 0;
  return Array.from({ length: n }, (_, i) => ({
    value: String(i),
    label: axLabel(i),
  }));
}

function fillSelect(sel, opts, selected){
  if (!sel) return;
  // remove any previous listeners by rebuilding the element
  sel.innerHTML = "";
  for (const {value, label} of opts){
    const o = document.createElement("option");
    o.value = value;
    o.textContent = label;
    sel.appendChild(o);
  }
  if (selected != null) sel.value = String(selected);
}

function onChangeNumber(el, set){
  if (!el) return;
  el.onchange = null; // clear previous
  el.addEventListener("change", () => {
    const v = Number(el.value);
    if (Number.isFinite(v)) set(v);
    drawPlots();
    updateCursor(state.cursorPoint);
  });
}

function show(el, v=true){ if (el) el.style.display = v ? "" : "none"; }

/* -----------------------------------------
   Shortcuts: only set data-* (CSS does rest)
   ----------------------------------------- */
export function refreshShortcuts(){
  const fs = dom.shortcutsFS;
  if (!fs) return;
  fs.dataset.mode = (state.inputSource === "keyboard") ? "keyboard" : "other";
  fs.dataset.dim  = String(state.dim);
}

/* ----------------------------------------------------
   Axis selectors setup (populate + visibility toggles)
   ---------------------------------------------------- */
export function setupAxisSelectors(){
  const dim = Number(state.dim) || 0;

  // groups visibility
  show(dom.singleAxisControls, dim <= 3);
  show(dom.dualAxisControls,   dim >  3);

  // Z label visibility within the 2D/3D group
  const zLabel = dom.selZ ? dom.selZ.closest("label") : null;
  show(zLabel, dim === 3); // show only in 3D

  // ensure axis state objects exist
  if (!state.currentAxes)  state.currentAxes  = { x:0, y:1, z:2 };
  if (!state.currentAxesA) state.currentAxesA = { x:0, y:1 };
  if (!state.currentAxesB) state.currentAxesB = { x:2, y:3 };

  const opts = optionList(dim);

  // --- populate selects
  // 2D/3D
  fillSelect(dom.selX, opts, state.currentAxes.x);
  fillSelect(dom.selY, opts, state.currentAxes.y);
  if (dim === 3) fillSelect(dom.selZ, opts, state.currentAxes.z);

  // 4D
  fillSelect(dom.selAX, opts, state.currentAxesA.x);
  fillSelect(dom.selAY, opts, state.currentAxesA.y);
  fillSelect(dom.selBX, opts, state.currentAxesB.x);
  fillSelect(dom.selBY, opts, state.currentAxesB.y);

  // --- listeners
  if (dim <= 3){
    onChangeNumber(dom.selX, v => state.currentAxes.x = v);
    onChangeNumber(dom.selY, v => state.currentAxes.y = v);
    if (dim === 3) onChangeNumber(dom.selZ, v => state.currentAxes.z = v);
  } else {
    onChangeNumber(dom.selAX, v => state.currentAxesA.x = v);
    onChangeNumber(dom.selAY, v => state.currentAxesA.y = v);
    onChangeNumber(dom.selBX, v => state.currentAxesB.x = v);
    onChangeNumber(dom.selBY, v => state.currentAxesB.y = v);
  }
}

/* -------------------------------------------------
   4D-specific UI wiring (safe no-op elsewhere)
   ------------------------------------------------- */
export function setupDual2DControls(){
  if (Number(state.dim) !== 4) return;

  // ensure defaults sane
  if (!state.currentAxesA) state.currentAxesA = { x:0, y:1 };
  if (!state.currentAxesB) state.currentAxesB = { x:2, y:3 };

  // ensure selectors reflect current state (e.g., if state set before UI)
  if (dom.selAX) dom.selAX.value = String(state.currentAxesA.x);
  if (dom.selAY) dom.selAY.value = String(state.currentAxesA.y);
  if (dom.selBX) dom.selBX.value = String(state.currentAxesB.x);
  if (dom.selBY) dom.selBY.value = String(state.currentAxesB.y);
}
