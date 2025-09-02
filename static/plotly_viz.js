/* global Plotly, io */

// Socket.IO
const socket = io();

// DOM
const plotEl = document.getElementById("plot-container");
const selInput = document.getElementById("input-source");
const selPoint = document.getElementById("point-select");
const selX = document.getElementById("axis-x");
const selY = document.getElementById("axis-y");
const selZ = document.getElementById("axis-z");
const wControls = document.getElementById("slice-controls");
const wSlider = document.getElementById("w-slider");
const wReadout = document.getElementById("w-value");

// colour placeholders — centralise styling here
const CURSOR_GLOW_SIZE = 18;
const CURSOR_GLOW_COLOR = "rgb(255,200,120)";
const CURSOR_GLOW_OPACITY = 0.25;
const CURSOR_DOT_SIZE = 7;
const CURSOR_DOT_COLOR = "rgb(255,210,150)";
const CURSOR_DOT_LINE = "#ffffff";
const MARKER_COLOR = "#6ea8fe";
const BG_COLOR = "#101214";


// State
let latent = [];         // NxD
let dim = 0;             // D
let boundsMin = [];
let boundsMax = [];
let axisNames = [];      // ["z0","z1","z2","z3"]
let currentAxes = { x:0, y:1, z:2 };
let inputSource = "osc"; // "osc" | "mouse"
let is3D = false;
let cursorPoint = null;     // array length D
let cursorTraceIndex = 1;   // set by drawPlot
let sliceW0 = null;         // 4D slicing centre (latent coord along slice dim)
let sliceDim = null;        // which latent dimension is used for slicing (4D only)
let wValue = 0.0;
let keyNavEnabled = false;
let localSeq = 0;
let lastAppliedSeq = -1;
let cursorGlowIdx = -1;
let cursorDotIdx = -1;

// Keyboard step size
const STEP_BASE =  0.03; // normal
const STEP_FINE =  0.01; // alt
const STEP_COARSE = 0.1; // shift

function currentStep(e) {
    if (e && e.shiftKey) return STEP_COARSE;
    if (e && e.altKey) return STEP_FINE;
    return STEP_BASE;
}


// Utilities
function populateSelect(el, n, selectedIdx=0, labels=null) {
  el.innerHTML = "";
  for (let i=0; i<n; i++) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = labels ? labels[i] : "z" + i;
    if (i === selectedIdx) opt.selected = true;
    el.appendChild(opt);
  }
}

function updateControlsVisibility() {
  const zEls = document.querySelectorAll(".z-only, #axis-z");
  if (dim === 2) {
    zEls.forEach(e => e.style.display = "none");
  } else {
    zEls.forEach(e => e.style.display = "");
  }
  if (wControls) wControls.style.display = (dim === 4 ? "flex" : "none");
}

function buildAxisNames(n) {
  axisNames = Array.from({length:n}, (_,i) => "z" + i);
}

function getColumn(arr, idx) {
  return arr.map(row => row[idx]);
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

// Map latent coordinate -> normalised cursor u in [-1,1]
function latentToU(val, dimIdx) {
  const lo = boundsMin[dimIdx], hi = boundsMax[dimIdx];
  const denom = Math.max(1e-12, (hi - lo));
  const u = 2.0 * (val - lo) / denom - 1.0;
  return clamp(u, -1.0, 1.0);
}

// Map normalised cursor u in [-1,1] -> latent coordinate
function uToLatent(u, dimIdx) {
  const lo = boundsMin[dimIdx], hi = boundsMax[dimIdx];
  return (u + 1.0) * 0.5 * (hi - lo) + lo;
}

function clamp01(x) { return Math.min(1, Math.max(-1, x)); }


// Send cursor in normalised space to backend via Socket.IO
function sendCursor(latentPoint) {
  const u = new Array(dim);
  for (let j=0; j<dim; j++) u[j] = latentToU(latentPoint[j], j);
  localSeq += 1;
  socket.emit("cursor_move", { u, origin: inputSource, seq: localSeq});
}

function buildUFromCursor(p) {
  const u = new Array(dim);
  for (let j = 0; j < dim; j++) u[j] = latentToU(p[j], j);
  return u;
}

function applyUToCursor(u) {
  const next = new Array(dim);
  for (let j = 0; j < dim; j++) next[j] = uToLatent(u[j], j);
  cursorPoint = next;
  updateCursor(cursorPoint);
  sendCursor(cursorPoint);
}

function handleKeyDown(e) {
  if (!keyNavEnabled || !cursorPoint) return;

  // do not hijack typing in inputs
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
  if (tag === "input" || tag === "select" || tag === "textarea") return;

  const step = currentStep(e);
  let used = false;

  // u from current cursor
  const u = buildUFromCursor(cursorPoint);

  // X (←/→ or A/D)
  if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
    u[currentAxes.x] = clamp(u[currentAxes.x] - step, -1, 1); used = true;
  } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
    u[currentAxes.x] = clamp(u[currentAxes.x] + step, -1, 1); used = true;
  }

  // Y (↑/↓ or W/S)
  if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
    u[currentAxes.y] = clamp(u[currentAxes.y] + step, -1, 1); used = true;
  } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
    u[currentAxes.y] = clamp(u[currentAxes.y] - step, -1, 1); used = true;
  }

  // Z (PageUp/PageDown or E/Q) — only if present
  if (dim >= 3 && typeof currentAxes.z === "number") {
    if (e.key === "PageUp" || e.key === "e" || e.key === "E") {
      u[currentAxes.z] = clamp(u[currentAxes.z] + step, -1, 1); used = true;
    } else if (e.key === "PageDown" || e.key === "q" || e.key === "Q") {
      u[currentAxes.z] = clamp(u[currentAxes.z] - step, -1, 1); used = true;
    }
  }

  // W (4D slice via slider semantics) — [ / ]
  if (dim === 4 && sliceDim != null) {
    if (e.key === "]") {
      u[sliceDim] = clamp(u[sliceDim] + step, -1, 1); used = true;
    } else if (e.key === "[") {
      u[sliceDim] = clamp(u[sliceDim] - step, -1, 1); used = true;
    }
    if (used) {
      // keep slider/readout and plot split in sync
      if (wSlider)  wSlider.value = String(u[sliceDim]);
      if (wReadout) wReadout.textContent = u[sliceDim].toFixed(2);
      sliceW0 = uToLatent(u[sliceDim], sliceDim);
      drawPlot();
    }
  }

  if (used) {
    e.preventDefault(); // avoid page scroll with arrows
    applyUToCursor(u);
    lastAppliedSeq = localSeq;
  }
}

function handleKeyUp(_e) {
  // reserved for future use (custom repeats, etc.)
}



// Build Plotly traces; in 4D we slice along the 4th dim via opacity masks.
function makeScatterTraces() {
  const axX = currentAxes.x;
  const axY = currentAxes.y;
  const axZ = currentAxes.z;

  // Columns for the currently selected axes
  const x = getColumn(latent, axX);
  const y = getColumn(latent, axY);

  // Cursor defaults (centre if not available)
  const cx = (cursorPoint && cursorPoint.length)
    ? cursorPoint[axX]
    : 0.5 * (boundsMin[axX] + boundsMax[axX]);
  const cy = (cursorPoint && cursorPoint.length)
    ? cursorPoint[axY]
    : 0.5 * (boundsMin[axY] + boundsMax[axY]);
  const cz = (typeof axZ === "number" && cursorPoint && cursorPoint.length)
    ? cursorPoint[axZ]
    : 0.0;

  const traces = [];
  let layout;
  let is3D = false;

  // ---------------- 2D ----------------
  if (dim === 2) {
    const pts2d = {
      type: "scattergl",
      mode: "markers",
      x, y,
      marker: {
        size: 6,
        color: MARKER_COLOR // colour placeholder
      },
      name: "anchors"
    };

    const cursorGlow2d = {
      type: "scattergl",
      mode: "markers",
      x: [cx], y: [cy],
      marker: {
        size: CURSOR_GLOW_SIZE,
        opacity: CURSOR_GLOW_OPACITY,
        color: CURSOR_GLOW_COLOR // colour placeholder
      },
      hoverinfo: "skip",
      showlegend: false
    };

    const cursorDot2d = {
      type: "scattergl",
      mode: "markers",
      x: [cx], y: [cy],
      marker: {
        size: CURSOR_DOT_SIZE,
        color: CURSOR_DOT_COLOR, // colour placeholder
        line: { width: 2, color: CURSOR_DOT_LINE }, // colour placeholder
        symbol: "circle"
      },
      hoverinfo: "skip",
      showlegend: false
    };

    traces.push(pts2d, cursorGlow2d, cursorDot2d);

    layout = {
      dragmode: "pan",
      hovermode: "closest",
      xaxis: { title: axisNames[axX] },
      yaxis: { title: axisNames[axY] },
      margin: { t: 10, r: 10, b: 40, l: 40 },
      paper_bgcolor: BG_COLOR, // colour placeholder
      plot_bgcolor: BG_COLOR   // colour placeholder
    };

    return {
      traces,
      layout,
      is3D: false,
      cursorIndices: { glow: traces.length - 2, dot: traces.length - 1 }
    };
  }

  // ---------------- 3D / 4D ----------------
  const z = getColumn(latent, axZ);

  if (dim === 4 && sliceDim != null) {
    // Simple slice around sliceW0 (tune the half-width if desired)
    const HALF_W = 0.12; // slice half-width in latent units (colour placeholder param)
    const near = { x: [], y: [], z: [] };
    const far  = { x: [], y: [], z: [] };

    for (let i = 0; i < latent.length; i++) {
      const wVal = latent[i][sliceDim];
      const tgt = (Math.abs(wVal - sliceW0) <= HALF_W) ? near : far;
      tgt.x.push(x[i]); tgt.y.push(y[i]); tgt.z.push(z[i]);
    }

    traces.push({
      type: "scatter3d",
      mode: "markers",
      x: near.x, y: near.y, z: near.z,
      marker: {
        size: 3,
        color: near.z.length === z.length ? z : near.z, // fall back if all near
        colorscale: "Viridis", // colour placeholder
        showscale: false,
        opacity: 1.0
      },
      name: "anchors (slice)"
    });

    traces.push({
      type: "scatter3d",
      mode: "markers",
      x: far.x, y: far.y, z: far.z,
      marker: {
        size: 3,
        color: far.z.length === z.length ? z : far.z,
        colorscale: "Viridis", // colour placeholder
        showscale: false,
        opacity: 0.10
      },
      name: "anchors (off-slice)"
    });
  } else {
    // Plain 3D
    traces.push({
      type: "scatter3d",
      mode: "markers",
      x, y, z,
      marker: {
        size: 3,
        color: z,                 // depth cue
        colorscale: "Viridis",    // colour placeholder
        showscale: false
      },
      name: "anchors"
    });
  }

  const cursorGlow3d = {
    type: "scatter3d",
    mode: "markers",
    x: [cx], y: [cy], z: [cz],
    marker: {
      size: CURSOR_GLOW_SIZE,
      opacity: CURSOR_GLOW_OPACITY,
      color: CURSOR_GLOW_COLOR // colour placeholder
    },
    hoverinfo: "skip",
    showlegend: false
  };

  const cursorDot3d = {
    type: "scatter3d",
    mode: "markers",
    x: [cx], y: [cy], z: [cz],
    marker: {
      size: CURSOR_DOT_SIZE,
      color: CURSOR_DOT_COLOR, // colour placeholder
      line: { width: 2, color: CURSOR_DOT_LINE }, // colour placeholder
      symbol: "circle"
    },
    hoverinfo: "skip",
    showlegend: false
  };

  traces.push(cursorGlow3d, cursorDot3d);

  layout = {
    scene: {
      xaxis: { title: axisNames[axX] },
      yaxis: { title: axisNames[axY] },
      zaxis: { title: axisNames[axZ] },
      bgcolor: BG_COLOR // colour placeholder
    },
    margin: { t: 10, r: 10, b: 10, l: 10 },
    paper_bgcolor: BG_COLOR // colour placeholder
  };

  is3D = true;

  return {
    traces,
    layout,
    is3D,
    cursorIndices: { glow: traces.length - 2, dot: traces.length - 1 }
  };
}


function drawPlot() {
  const { traces, layout, cursorIndices} = makeScatterTraces();
  Plotly.react(plotEl, traces, layout, { responsive: true});

  cursorGlowIdx = cursorIndices.glow;
  cursorDotIdx = cursorIndices.dot;
}

function updateCursor(latentPoint) {
  if (!latentPoint || !Array.isArray(latentPoint) || latentPoint.length !== dim) return;
  
  // Read cohordinates onth currently selected axes
  const cx = latentPoint[currentAxes.x];
  const cy = latentPoint[currentAxes.y];

  if (!is3D) {
    // 2D; update (x,y) for both halo and dot
    if (cursorGlowIdx >= 0) {
        Plotly.restyle(plotEl, { x: [[cx]], y: [[cy]]}, [cursorGlowIdx]);
    }
    if (cursorDotIdx >= 0) {
        Plotly.restyle(plotEl, { x: [[cx]], y: [[cy]]}, [cursorDotIdx]);
    }
    return;
  }

  // 3D / 4D: update (x,y,z). If z-axis not set, fall back to 0.
  const cz = (typeof currentAxes.z === "number") ? latentPoint[currentAxes.z] : 0.0;

  if (cursorGlowIdx >= 0) {
    Plotly.restyle(plotEl, { x: [[cx]], y: [[cy]], z: [[cz]] }, [cursorGlowIdx]);
  }
  if (cursorDotIdx >= 0) {
    Plotly.restyle(plotEl, { x: [[cx]], y: [[cy]], z: [[cz]] }, [cursorDotIdx]);
  }
}


// Re-apply the slice (4D) given a new w0 (called on OSC updates or axis changes)
function applySliceFromLatent(latentPoint) {
  if (dim !== 4) return;
  // w0 = latentPoint on sliceDim
  sliceW0 = latentPoint[sliceDim];
  if (wSlider && wReadout) {
    wValue = latentToU(sliceW0, sliceDim);
    wSlider.value = String(wValue);
    wReadout.textContent = wValue.toFixed(2);
  }
  drawPlot();                // rebuild anchors split
  updateCursor(latentPoint); // keep cursor where it is
}

// Mouse click → move cursor (only when inputSource === "mouse")
plotEl.addEventListener("plotly_click", (ev) => {
  if (inputSource !== "mouse") return;
  if (!ev || !ev.points || !ev.points.length) return;

  const p = ev.points[0];

  if (!is3D) {
    const latentPoint = Array.from({length: dim}, (_,i) => {
      if (i === currentAxes.x) return p.x;
      if (i === currentAxes.y) return p.y;
      const lo = boundsMin[i], hi = boundsMax[i];
      return 0.5 * (lo + hi);
    });
    cursorPoint = latentPoint;
  } else {
    const latentPoint = Array.from({length: dim}, (_,i) => {
      if (i === currentAxes.x) return p.x;
      if (i === currentAxes.y) return p.y;
      if (i === currentAxes.z) return p.z;
      const lo = boundsMin[i], hi = boundsMax[i];
      return 0.5 * (lo + hi);
    });
    cursorPoint = latentPoint;
    if (dim === 4) applySliceFromLatent(cursorPoint);
  }

  updateCursor(cursorPoint);
  sendCursor(cursorPoint);
});

// Axis mapping controls
function syncAxisSelectors() {
  populateSelect(selX, dim, 0, axisNames);
  populateSelect(selY, dim, 1, axisNames);
  if (dim >= 3) populateSelect(selZ, dim, Math.min(2, dim-1), axisNames);

  updateControlsVisibility();

  selX.addEventListener("change", () => { currentAxes.x = Number(selX.value); drawPlot(); if (cursorPoint) updateCursor(cursorPoint); });
  selY.addEventListener("change", () => { currentAxes.y = Number(selY.value); drawPlot(); if (cursorPoint) updateCursor(cursorPoint); });
  selZ.addEventListener("change", () => { currentAxes.z = Number(selZ.value); drawPlot(); if (cursorPoint) updateCursor(cursorPoint); });
}

// Input source menu
selInput.addEventListener("change", () => {
  inputSource = selInput.value; // "osc" | "mouse" | "keyboard"
  if (inputSource === "keyboard") {
    if (!keyNavEnabled) {
      window.addEventListener("keydown", handleKeyDown, { passive: false });
      window.addEventListener("keyup",   handleKeyUp,   { passive: true  });
      keyNavEnabled = true;
    }
  } else {
    if (keyNavEnabled) {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup",   handleKeyUp);
      keyNavEnabled = false;
    }
  }
});

// Point selection menu → jump to that point and send
selPoint.addEventListener("change", () => {
  const v = selPoint.value;
  if (v === "") return;
  const idx = Number(v);
  if (!Number.isFinite(idx) || idx < 0 || idx >= latent.length) return;
  cursorPoint = latent[idx].slice();
  if (dim === 4) applySliceFromLatent(cursorPoint);
  updateCursor(cursorPoint);
  sendCursor(cursorPoint);
});

// W slider → updates slice centre (in latent coords) and UI; sends cursor only in mouse mode
if (wSlider && wReadout) {
  wSlider.addEventListener("input", () => {
    wValue = parseFloat(wSlider.value) || 0.0; // [-1, 1]
    wReadout.textContent = wValue.toFixed(2);
    if (dim === 4 && sliceDim != null) {
      // update slice centre in latent space
      sliceW0 = uToLatent(wValue, sliceDim);

      // keep cursor’s W aligned to the slice (preserve other coords)
      if (cursorPoint && cursorPoint.length === dim) {
        cursorPoint[sliceDim] = sliceW0;
        updateCursor(cursorPoint);
        if (inputSource === "mouse") {
          sendCursor(cursorPoint);
        }
      }
      // re-split anchors with new slice
      drawPlot();
    }
  });
}

// Listen for server-driven cursor updates (OSC → UI sync)
socket.on("cursor_update", (payload) => {
  try {
    // ---dedup a sequence-id ---
    const seq = (payload && typeof payload.seq === "number") ? payload.seq : null;
    if (seq !== null && seq <= lastAppliedSeq) {
        if (payload && Array.isArray(payload.y)) {
            console.log("RBF reconstructed:", payload.y);
        }
        return
    }

    const u = payload && payload.u;
    if (!u || !Array.isArray(u)) return;
    if (u.length !== dim) return;

    // Convert u in [-1,1]^d to latent space
    const lp = u.map((uu, i) => uToLatent(uu, i));
    cursorPoint = lp;
    if (dim === 4) applySliceFromLatent(cursorPoint);
    updateCursor(cursorPoint);

    if (seq !== null) lastAppliedSeq = seq;

    if (payload && Array.isArray(payload.y)) {
        console.log("RBF reconstructed:", payload.y);
    }
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error("cursor_update error:", err);
  }
});

// Boot
(async function init() {
  // Fetch latent data + meta
  const resp = await fetch("/data");
  const meta = await resp.json();
  latent = meta.latent;
  dim = meta.dim;
  boundsMin = meta.bounds_min;
  boundsMax = meta.bounds_max;

  buildAxisNames(dim);
  syncAxisSelectors();

  if (dim === 4) {
    const used = new Set([currentAxes.x, currentAxes.y]);
    if (typeof currentAxes.z === "number") used.add(currentAxes.z);
    const all = [0, 1, 2, 3];
    sliceDim = all.find(i => !used.has(i)) ?? 3;

  // mostra i controlli W (lo slider)
  if (wControls) {
    wControls.style.display = "flex";
    wSlider.value = "0";
    wValue = 0.0;
    wReadout.textContent = wValue.toFixed(2);
  }
} else {
  sliceDim = null;
  if (wControls) wControls.style.display = "none";
}

  inputSource = (selInput && selInput.value) ? selInput.value : inputSource

  // Fill point selector
  selPoint.innerHTML = '<option value="">— select point —</option>';
  for (let i=0; i<latent.length; i++) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = `Point ${i}`;
    selPoint.appendChild(opt);
  }

  drawPlot();

  // Start cursor at first point (or centre if empty)
  if (latent.length > 0) {
    cursorPoint = latent[0].slice();
  } else {
    cursorPoint = Array.from({length: dim}, (_,i) => 0.5*(boundsMin[i]+boundsMax[i]));
  }
  if (dim === 4) applySliceFromLatent(cursorPoint);
  updateCursor(cursorPoint);

  if (selInput) selInput.dispatchEvent(new Event("change"));

  // In OSC mode, immediately send the current cursor once to prime the pipeline
  if (inputSource === "osc") {
    sendCursor(cursorPoint);
  }
})();
