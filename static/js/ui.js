// /static/js/ui.js
import { state, populateSelect, updateControlVisibility } from "./core.js";
import { drawPlots, updateCursor } from "./plot.js";

export const dom = {
  selInput: document.getElementById("input-source"),
  selPoint: document.getElementById("preset-select"),

  // 2D/3D
  selX: document.getElementById("axis-x"),
  selY: document.getElementById("axis-y"),
  selZ: document.getElementById("axis-z"),

  // 4D
  selAX: document.getElementById("axis-a-x"),
  selAY: document.getElementById("axis-a-y"),
  selBX: document.getElementById("axis-b-x"),
  selBY: document.getElementById("axis-b-y"),

  // shortcuts
  shortcutsFS: document.getElementById("shortcuts"),
  shortcutsBody: document.getElementById("shortcuts-body"),
};

// opzioni per assi: value numerico "0..D-1", label "x,y,z,w"
function axisOptionObjects(){
  return Array.from({ length: state.dim }, (_, i) => ({
    value: String(i),
    label: state.axisNames[i] ?? `z${i}`,
  }));
}

export function setupAxisSelectors() {
  updateControlVisibility(state.dim);

  const opts = axisOptionObjects();

  if (state.dim <= 3) {
    // 2D/3D
    populateSelect(dom.selX, opts, state.currentAxes.x);
    populateSelect(dom.selY, opts, state.currentAxes.y);
    if (state.dim === 3 && dom.selZ) {
      populateSelect(dom.selZ, opts, state.currentAxes.z);
    }

    dom.selX?.addEventListener("change", () => {
      state.currentAxes.x = Number(dom.selX.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
    dom.selY?.addEventListener("change", () => {
      state.currentAxes.y = Number(dom.selY.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
    dom.selZ?.addEventListener("change", () => {
      state.currentAxes.z = Number(dom.selZ.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
  } else {
    // 4D (due viste 2D)
    populateSelect(dom.selAX, opts, state.currentAxesA.x);
    populateSelect(dom.selAY, opts, state.currentAxesA.y);
    populateSelect(dom.selBX, opts, state.currentAxesB.x);
    populateSelect(dom.selBY, opts, state.currentAxesB.y);

    dom.selAX?.addEventListener("change", () => {
      state.currentAxesA.x = Number(dom.selAX.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
    dom.selAY?.addEventListener("change", () => {
      state.currentAxesA.y = Number(dom.selAY.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
    dom.selBX?.addEventListener("change", () => {
      state.currentAxesB.x = Number(dom.selBX.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
    dom.selBY?.addEventListener("change", () => {
      state.currentAxesB.y = Number(dom.selBY.value);
      drawPlots(); updateCursor(state.cursorPoint);
    });
  }
}

export function refreshShortcuts() {
  const fs = dom.shortcutsFS;
  if (!fs) return;

  // mostra solo se input = keyboard
  const isKb = state.inputSource === "keyboard";
  fs.style.display = isKb ? "" : "none";
  if (!isKb) return;

  let html = "";
  if (state.dim === 2) {
    html = `
      <div><kbd class="kbd">A/D</kbd> <kbd class="kbd">W/S</kbd> → move</div>
      <div><kbd class="kbd">Shift</kbd> coarse, <kbd class="kbd">Alt</kbd> fine</div>`;
  } else if (state.dim === 3) {
    html = `
      <div><kbd class="kbd">A/D</kbd> (x), <kbd class="kbd">W/S</kbd> (y), <kbd class="kbd">Q/E</kbd> (z)</div>
      <div><kbd class="kbd">Shift</kbd> coarse, <kbd class="kbd">Alt</kbd> fine</div>`;
  } else {
    html = `
      <div><strong>View A</strong> → <kbd class="kbd">A/D</kbd>, <kbd class="kbd">W/S</kbd></div>
      <div><strong>View B</strong> → <kbd class="kbd">F/H</kbd>, <kbd class="kbd">T/G</kbd></div>
      <div><kbd class="kbd">Shift</kbd> coarse, <kbd class="kbd">Alt</kbd> fine</div>`;
  }
  dom.shortcutsBody.innerHTML = html;
}
