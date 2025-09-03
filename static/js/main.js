// main.js
/* global Plotly */
import {
  state, CONST, clamp, clamp11, currentStep, buildAxisNames,
  latentToU, uToLatent
} from "./core.js";
import { dom, syncAxisSelectors } from "./ui.js";
import { drawPlot, updateCursor, applySliceFromLatent } from "./plot.js";
import { sendCursor, setupSocket } from "./net.js";

// Keyboard handlers
function handleKeyDown(e) {
  if (!state.keyNavEnabled || !state.cursorPoint) return;
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
  if (tag === "input" || tag === "select" || tag === "textarea") return;

  const step = currentStep(e);
  let used = false;

  // u corrente ricavato dal marker visibile
  const u = state.uCurrent.slice();

  // X (←/→ o A/D)
  if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
    u[state.currentAxes.x] = clamp(u[state.currentAxes.x] - step, -1, 1); used = true;
  } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
    u[state.currentAxes.x] = clamp(u[state.currentAxes.x] + step, -1, 1); used = true;
  }

  // Y (↑/↓ o W/S)
  if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
    u[state.currentAxes.y] = clamp(u[state.currentAxes.y] + step, -1, 1); used = true;
  } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
    u[state.currentAxes.y] = clamp(u[state.currentAxes.y] - step, -1, 1); used = true;
  }

  // Z (PageUp/PageDown o E/Q) — solo se presente
  if (state.dim >= 3 && typeof state.currentAxes.z === "number") {
    if (e.key === "PageUp" || e.key === "e" || e.key === "E") {
      u[state.currentAxes.z] = clamp(u[state.currentAxes.z] + step, -1, 1); used = true;
    } else if (e.key === "PageDown" || e.key === "q" || e.key === "Q") {
      u[state.currentAxes.z] = clamp(u[state.currentAxes.z] - step, -1, 1); used = true;
    }
  }

  // W (slice 4D) — tasti [ / ]
  if (state.dim === 4 && state.sliceDim != null) {
    if (e.key === "]") {
      u[state.sliceDim] = clamp(u[state.sliceDim] + step, -1, 1); used = true;
    } else if (e.key === "[") {
      u[state.sliceDim] = clamp(u[state.sliceDim] - step, -1, 1); used = true;
    }
    if (used) {
      if (dom.wSlider)  dom.wSlider.value = String(u[state.sliceDim]);
      if (dom.wReadout) dom.wReadout.textContent = Number(u[state.sliceDim]).toFixed(2);
    }
  }

  if (used) {
    e.preventDefault();
    state.uTarget = u.map(v => clamp(v, -1, 1));
  }
}

function handleKeyUp(_e) { /* reserved for future use */ }

// Smoothing loop
function tickSmooth() {
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
    if (state.dim === 4) applySliceFromLatent(lp);
    updateCursor(lp);

    const now = (typeof performance !== "undefined" ? performance.now() : Date.now());
    if (now - state.lastSendTs >= CONST.SEND_INTERVAL_MS) {
      state.localSeq += 1;
      // Emit directly to keep same behaviour as original file (and dedup)
      const u = [...state.uCurrent];
      // socket emit without importing socket: reuse sendCursor-equivalent fields
      // but we need origin and seq fields identical to original:
      // We call sendCursor only to keep single source of truth for payload shape,
      // but then set lastAppliedSeq like the original did.
      const tmpLp = u.map((uu, j) => uToLatent(uu, j));
      sendCursor(tmpLp);
      state.lastAppliedSeq = state.localSeq;
      state.lastSendTs = now;
    }
  }
  requestAnimationFrame(tickSmooth);
}

// Boot
(async function init() {
  // Fetch latent data + meta
  const resp = await fetch("/data");
  const meta = await resp.json();
  state.latent = meta.latent;
  state.dim = meta.dim;
  state.boundsMin = meta.bounds_min;
  state.boundsMax = meta.bounds_max;

  buildAxisNames(state.dim);
  syncAxisSelectors(drawPlot, updateCursor);

  // Set cursor initial position
  state.uCurrent = new Array(state.dim).fill(0.0);
  state.uTarget  = new Array(state.dim).fill(0.0);

  // 4D slice dimension (unused axis among x,y,z)
  if (state.dim === 4) {
    const used = new Set([state.currentAxes.x, state.currentAxes.y]);
    if (typeof state.currentAxes.z === "number") used.add(state.currentAxes.z);
    const all = [0, 1, 2, 3];
    state.sliceDim = all.find(i => !used.has(i)) ?? 3;

    if (dom.wControls) {
      dom.wControls.style.display = "flex";
      dom.wSlider.value = "0";
      state.wValue = 0.0;
      dom.wReadout.textContent = state.wValue.toFixed(2);
    }
  } else {
    state.sliceDim = null;
    if (dom.wControls) dom.wControls.style.display = "none";
  }

  // Input source initial
  state.inputSource = (dom.selInput && dom.selInput.value) ? dom.selInput.value : state.inputSource;

  // Fill point selector
  dom.selPoint.innerHTML = '<option value="">— select point —</option>';
  for (let i = 0; i < state.latent.length; i++) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = `Point ${i}`;
    dom.selPoint.appendChild(opt);
  }

  drawPlot();

  // Persist camera between relayouts (3D)
  if (dom.plotEl && typeof dom.plotEl.on === "function") {
    dom.plotEl.on("plotly_relayout", (ev) => {
      if (ev && ev["scene.camera"] && typeof ev["scene.camera"] === "object") {
        state.lastCamera = ev["scene.camera"];
      } else if (ev && ev["scene_camera"]) {
        state.lastCamera = ev["scene_camera"];
      }
    });
  }

  // Initial cursor
  if (state.latent && state.latent.length > 0) {
    state.cursorPoint = state.latent[0].slice();
  } else {
    state.cursorPoint = Array.from({ length: state.dim }, (_, i) => 0.5 * (state.boundsMin[i] + state.boundsMax[i]));
  }
  if (state.dim === 4) applySliceFromLatent(state.cursorPoint);
  updateCursor(state.cursorPoint);

  // Input source menu
  dom.selInput.addEventListener("change", () => {
    state.inputSource = dom.selInput.value; // "osc" | "mouse" | "keyboard"
    if (state.inputSource === "keyboard") {
      if (!state.keyNavEnabled) {
        window.addEventListener("keydown", handleKeyDown, { passive: false });
        window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
        state.keyNavEnabled = true;
      }
    } else {
      if (state.keyNavEnabled) {
        window.removeEventListener("keydown", handleKeyDown);
        window.removeEventListener("keyup",   handleKeyUp);
        state.keyNavEnabled = false;
      }
    }
  });

  // Point selection menu
  dom.selPoint.addEventListener("change", () => {
    const v = dom.selPoint.value;
    if (v === "") return;
    const idx = Number(v);
    if (!Number.isFinite(idx) || idx < 0 || idx >= state.latent.length) return;
    state.cursorPoint = state.latent[idx].slice();
    if (state.dim === 4) applySliceFromLatent(state.cursorPoint);
    updateCursor(state.cursorPoint);
    sendCursor(state.cursorPoint);
  });

  // W slider
  if (dom.wSlider && dom.wReadout) {
    dom.wSlider.addEventListener("input", () => {
      state.wValue = parseFloat(dom.wSlider.value) || 0.0; // [-1,1]
      dom.wReadout.textContent = state.wValue.toFixed(2);
      if (state.dim === 4 && state.sliceDim != null) {
        // update slice centre in latent space
        state.sliceW0 = uToLatent(state.wValue, state.sliceDim);

        // keep cursor’s W aligned to the slice
        if (state.cursorPoint && state.cursorPoint.length === state.dim) {
          state.cursorPoint[state.sliceDim] = state.sliceW0;
          updateCursor(state.cursorPoint);
          if (state.inputSource === "mouse") {
            sendCursor(state.cursorPoint);
          }
        }
        drawPlot();
      }
    });
  }

  // Plot click → set target
  dom.plotEl.addEventListener("plotly_click", (ev) => {
    if (state.inputSource !== "mouse") return;
    if (!ev || !ev.points || !ev.points.length) return;

    const p = ev.points[0];
    const lp = new Array(state.dim);
    for (let i = 0; i < state.dim; i++) {
      if (i === state.currentAxes.x) {
        lp[i] = p.x;
      } else if (i === state.currentAxes.y) {
        lp[i] = p.y;
      } else if (state.is3D && i === state.currentAxes.z) {
        lp[i] = p.z;
      } else {
        const lo = state.boundsMin[i], hi = state.boundsMax[i];
        lp[i] = 0.5 * (lo + hi);
      }
    }

    if (state.dim === 4 && typeof state.sliceDim === "number") {
      const lo = state.boundsMin[state.sliceDim], hi = state.boundsMax[state.sliceDim];
      const denom = Math.max(1e-12, (hi - lo));
      const uSlice = 2.0 * (lp[state.sliceDim] - lo) / denom - 1.0;
      if (dom.wSlider)  dom.wSlider.value = String(uSlice);
      if (dom.wReadout) dom.wReadout.textContent = Number(uSlice).toFixed(2);
    }

    const u = lp.map((val, j) => latentToU(val, j));
    state.uTarget = u.map(v => clamp(v, -1, 1));
  });

  // Start smoothing animation loop
  requestAnimationFrame(tickSmooth);

  // Fire source change to install keyboard listeners if needed
  if (dom.selInput) dom.selInput.dispatchEvent(new Event("change"));

  // In OSC mode, immediately send the current cursor once to prime the pipeline
  if (state.inputSource === "osc") {
    sendCursor(state.cursorPoint);
  }

  // Socket listener → update UI
  setupSocket((lp) => {
    state.cursorPoint = lp;
    if (state.dim === 4) applySliceFromLatent(lp);
    updateCursor(lp);
  });
})();
