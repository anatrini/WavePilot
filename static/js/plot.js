// plot.js — presentational only (costruisce traces e layout, niente logica “core”)

/* ===== import dal core (non modifichiamo core.js ora) =====
   - state:      stato condiviso (latent, dim, bounds, axes correnti, ecc.)
   - els:        {left,right} -> contenitori dei plot
   - cssVar:     legge token CSS (no fallback/hardcode)
   - latentToU:  v∈[0,1] → u∈[-1,1] in base ai bounds (j-esima dimensione)
*/
import { state, els, cssVar, latentToU, clamp } from "./core.js";

/* =========================================================
   THEME HELPERS (tutto lo stile arriva dai CSS)
   ========================================================= */
// HSL → HEX (#rrggbb)

function hslToHex(h, s, l){
  h = (h % 360 + 360) % 360; s = clamp(s,0,1); l = clamp(l,0,1);
  const c = (1 - Math.abs(2*l - 1)) * s;
  const hp = h / 60;
  const x = c * (1 - Math.abs((hp % 2) - 1));
  let [r,g,b] = [0,0,0];
  if (0<=hp && hp<1) [r,g,b] = [c,x,0];
  else if (1<=hp && hp<2) [r,g,b] = [x,c,0];
  else if (2<=hp && hp<3) [r,g,b] = [0,c,x];
  else if (3<=hp && hp<4) [r,g,b] = [0,x,c];
  else if (4<=hp && hp<5) [r,g,b] = [x,0,c];
  else if (5<=hp && hp<6) [r,g,b] = [c,0,x];
  const m = l - c/2;
  const to255 = (v)=>Math.round((v+m)*255);
  return `#${[to255(r),to255(g),to255(b)].map(v=>v.toString(16).padStart(2,"0")).join("")}`;
}

// Colori 2D: Hue=atan2, Sat=radius, Lightness=fisso
function colorsFrom2D(X, Y){
  const L   = parseFloat(cssVar('--cc-2d-lightness'));
  const S0  = parseFloat(cssVar('--cc-2d-sat-min'));
  const S1  = parseFloat(cssVar('--cc-2d-sat-max'));
  const maxR = Math.SQRT2; // r massimo in [-1,1]^2
  const N = X.length;
  const out = new Array(N);
  for (let i=0;i<N;i++){
    const x = X[i], y = Y[i];
    const h = (Math.atan2(y, x) + Math.PI) / (2*Math.PI) * 360; // 0..360
    const r = Math.hypot(x, y) / maxR;                          // 0..1
    const s = S0 + (S1 - S0) * clamp(r, 0, 1);
    out[i] = hslToHex(h, s, L);
  }
  return out;
}

// Colori 3D: RGB(x,y,z) con gamma
function colorsFrom3D(X, Y, Z){
  const g = parseFloat(cssVar('--cc-3d-gamma'));
  const N = X.length;
  const out = new Array(N);
  for (let i=0;i<N;i++){
    let r = (X[i]+1)/2, g1 = (Y[i]+1)/2, b = (Z[i]+1)/2;   // 0..1
    if (Number.isFinite(g) && g>0) { r = r**g; g1 = g1**g; b = b**g; }
    out[i] = `rgb(${Math.round(r*255)},${Math.round(g1*255)},${Math.round(b*255)})`;
  }
  return out;
}



export function applyPlotTheme2D(layout) {
  // sfondi
  layout.paper_bgcolor = cssVar('--plot-paper');
  layout.plot_bgcolor  = cssVar('--plot-bg');

  // tipografia
  const UIFONT = cssVar('--font-ui');
  const TXT    = cssVar('--plot-text');
  layout.font  = { ...(layout.font||{}), family: UIFONT, color: TXT };

  // assi, griglia, spike
  const GRID   = cssVar('--plot-grid');
  const AXIS   = cssVar('--plot-axis');
  const SPIKE  = cssVar('--spike-color');
  const ST     = Number(cssVar('--spike-thickness')) || undefined;
  const GW     = Number(cssVar('--grid-width'))      || undefined;

  const ATC = cssVar('--axis-title-color') || AXIS;
  const ATS = Number(cssVar('--axis-title-size')) || undefined;
  const TKS = Number(cssVar('--axis-tick-size'))  || undefined;

  layout.xaxis = {
    ...(layout.xaxis || {}),
    gridcolor: GRID, gridwidth: GW, linecolor: AXIS,
    spikecolor: SPIKE, spikethickness: ST, showspikes: true,
    titlefont: { family: UIFONT, color: ATC, size: ATS },
    tickfont:  { family: UIFONT, color: ATC, size: TKS },
  };
  layout.yaxis = {
    ...(layout.yaxis || {}),
    gridcolor: GRID, gridwidth: GW, linecolor: AXIS,
    spikecolor: SPIKE, spikethickness: ST, showspikes: true,
    titlefont: { family: UIFONT, color: ATC, size: ATS },
    tickfont:  { family: UIFONT, color: ATC, size: TKS },
  };

  // hoverlabel coerente
  layout.hoverlabel = {
    ...(layout.hoverlabel || {}),
    bgcolor: cssVar('--hover-bg'),
    bordercolor: cssVar('--hover-border'),
    font: { family: UIFONT, color: cssVar('--hover-text'),
            size: Number(cssVar('--hover-size')) || undefined }
  };

  // mai legenda
  layout.showlegend = false;
}

export function applyPlotTheme3D(layout) {
  // sfondi
  layout.paper_bgcolor = cssVar('--plot-paper');
  const UIFONT = cssVar('--font-ui');
  const TXT    = cssVar('--plot-text');
  layout.font  = { ...(layout.font||{}), family: UIFONT, color: TXT };

  // assi/griglia/spike
  const GRID  = cssVar('--plot-grid');
  const AXIS  = cssVar('--plot-axis');
  const SPIKE = cssVar('--spike-color');
  const ST    = Number(cssVar('--spike-thickness')) || undefined;
  const GW    = Number(cssVar('--grid-width'))      || undefined;

  const ATC = cssVar('--axis-title-color') || AXIS;
  const ATS = Number(cssVar('--axis-title-size')) || undefined;
  const TKS = Number(cssVar('--axis-tick-size'))  || undefined;

  const patchAxis = (ax) => ({
    ...(ax || {}),
    gridcolor: GRID, gridwidth: GW, color: AXIS,
    spikecolor: SPIKE, spikethickness: ST, showspikes: true,
    titlefont: { family: UIFONT, color: ATC, size: ATS },
    tickfont:  { family: UIFONT, color: ATC, size: TKS },
  });

  layout.margin = { l: 0, r: 0, t: 0, b: 0, pad: 0 };

  layout.scene = {
    ...(layout.scene || {}),
    bgcolor: cssVar('--plot-bg'),
    xaxis: patchAxis(layout.scene?.xaxis),
    yaxis: patchAxis(layout.scene?.yaxis),
    zaxis: patchAxis(layout.scene?.zaxis),
    camera: {
        center: {x: 0, y: 0, z: 0},
        up:     {x: 0, y: 0, z: 1},
        eye:    {x: 1.6, y: -1.6, z: 1.}
    }
  };

  layout.uirevision = 'keep-cam';
  layout.scene.aspectmode = 'cube';
  layout.scene.domain = { x: [0, 1], y: [0, 1] };

  // hoverlabel coerente
  layout.hoverlabel = {
    ...(layout.hoverlabel || {}),
    bgcolor: cssVar('--hover-bg'),
    bordercolor: cssVar('--hover-border'),
    font: { family: UIFONT, color: cssVar('--hover-text'),
            size: Number(cssVar('--hover-size')) || undefined }
  };

  layout.showlegend = false;
}

/* =========================================================
   DATA HELPERS
   ========================================================= */
// Estrae coordinate u∈[-1,1] per un paio/terzetto di assi da state.latent
function project2D(axX, axY) {
  const X = [], Y = [];
  const N = state.latent.length;
  for (let i = 0; i < N; i++) {
    const row = state.latent[i];
    X.push(latentToU(row[axX], axX, state.boundsMin, state.boundsMax));
    Y.push(latentToU(row[axY], axY, state.boundsMin, state.boundsMax));
  }
  return { X, Y };
}
function project3D(axX, axY, axZ) {
  const X = [], Y = [], Z = [];
  const N = state.latent.length;
  for (let i = 0; i < N; i++) {
    const row = state.latent[i];
    X.push(latentToU(row[axX], axX, state.boundsMin, state.boundsMax));
    Y.push(latentToU(row[axY], axY, state.boundsMin, state.boundsMax));
    Z.push(latentToU(row[axZ], axZ, state.boundsMin, state.boundsMax));
  }
  return { X, Y, Z };
}

/* =========================================================
   TRACES FACTORY (2D/3D) — no stile hard-coded
   ========================================================= */
function traces2D(axX, axY) {
  const { X, Y } = project2D(axX, axY);
  const colors = colorsFrom2D(X, Y);

  const pts = {
    type: "scattergl",
    mode: "markers",
    x: X, y: Y,
    marker: { 
        size: Number(cssVar('--point-size-2d')),
        color: colors,
        line: { color: cssVar('--point-stroke'), width: Number(cssVar('--point-stroke-width')) }
    },
    showlegend: false,
    hovertemplate: "x: %{x}<br>y: %{y}<extra></extra>",
  };

  const labels = {
    type: "scattergl",
    mode: "text",
    x: X, y: Y,
    text: state.presetNames || [],
    textposition: "top center",
    textfont: { family: cssVar('--font-ui'), color: cssVar('--plot-text'), size: 12 },
    showlegend: false,
    hoverinfo: "skip",
  };

  // cursore (glow + dot) — indici usati da updateCursor
  const glow = {
    type: "scattergl", mode: "markers",
    x: [0], y: [0],
    marker: {
      size: Number(cssVar('--cursor-glow-size')),
      color: cssVar('--cursor-glow-color'),
      opacity: Number(cssVar('--cursor-glow-opacity')),
    },
    hoverinfo: "skip", showlegend: false,
  };
  const dot = {
    type: "scattergl", mode: "markers",
    x: [0], y: [0],
    marker: {
      size: Number(cssVar('--cursor-dot-size')),
      color: cssVar('--cursor-dot-color'),
      line: { color: cssVar('--cursor-dot-line'), width: 1 },
    },
    hoverinfo: "skip", showlegend: false,
  };

  const traces = [pts, labels, glow, dot];
  const layout = {
    xaxis: { title: "x", range: [-1, 1] },
    yaxis: { title: "y", range: [-1, 1] },
    margin: { l: 30, r: 10, t: 10, b: 30 },
  };
  applyPlotTheme2D(layout);
  return { traces, layout, glowIdx: 2, dotIdx: 3 };
}

function traces3D(axX, axY, axZ) {
  const { X, Y, Z } = project3D(axX, axY, axZ);
  const colors = colorsFrom3D(X, Y, Z);

  const pts = {
    type: "scatter3d",
    mode: "markers",
    x: X, y: Y, z: Z,
    marker: { 
        size: Number(cssVar('--point-size-3d')),   
        color: colors,
        line: { color: cssVar('--point-stroke'), width: Number(cssVar('--point-stroke-width')) }
    },
    showlegend: false,
    hovertemplate: "x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>",
  };

  const labels = {
    type: "scatter3d",
    mode: "text",
    x: X, y: Y, z: Z,
    text: state.presetNames || [],
    textposition: "top center",
    textfont: { family: cssVar('--font-ui'), color: cssVar('--plot-text'), size: 11 },
    showlegend: false,
    hoverinfo: "skip",
  };

  const glow = {
    type: "scatter3d", mode: "markers",
    x: [0], y: [0], z: [0],
    marker: {
      size: Number(cssVar('--cursor-glow-size')),
      color: cssVar('--cursor-glow-color'),
      opacity: Number(cssVar('--cursor-glow-opacity')),
    },
    hoverinfo: "skip", showlegend: false,
  };
  const dot = {
    type: "scatter3d", mode: "markers",
    x: [0], y: [0], z: [0],
    marker: {
      size: Number(cssVar('--cursor-dot-size')),
      color: cssVar('--cursor-dot-color'),
      line: { color: cssVar('--cursor-dot-line'), width: 1 },
    },
    hoverinfo: "skip", showlegend: false,
  };

  const traces = [pts, labels, glow, dot];
  const layout = {
    scene: {
      xaxis: { title: "x", range: [-1, 1] },
      yaxis: { title: "y", range: [-1, 1] },
      zaxis: { title: "z", range: [-1, 1] },
    },
    margin: { l: 0, r: 0, t: 0, b: 0 },
  };
  applyPlotTheme3D(layout);
  return { traces, layout, glowIdx: 2, dotIdx: 3 };
}

/* =========================================================
   RENDERERS
   ========================================================= */
const CONFIG = { responsive: true, displaylogo: false };

function render2D(container, axX, axY) {
  const { traces, layout, glowIdx, dotIdx } = traces2D(axX, axY);
  Plotly.purge(container);
  Plotly.newPlot(container, traces, layout, CONFIG);
  return { glowIdx, dotIdx };
}
function render3D(container, axX, axY, axZ) {
  const { traces, layout, glowIdx, dotIdx } = traces3D(axX, axY, axZ);
  Plotly.purge(container);
  Plotly.newPlot(container, traces, layout, CONFIG);
  return { glowIdx, dotIdx };
}

/* =========================================================
   API PUBBLICA
   ========================================================= */
export function drawPlots() {
  const { left, right } = els();
  if (!left || !right) return;

  // 1) Modalità griglia: 2D/3D = singola colonna, 4D = due colonne
  const plotsEl = document.getElementById("plots");
  if (plotsEl) plotsEl.classList.toggle("dual", state.dim === 4);

  // 2) reset indici cursori
  state.cursorLeft  = null;
  state.cursorRight = null;

  // 3) render in base alla dimensionalità (nessun show/hide via JS: pensa il CSS)
  if (state.dim === 2) {
    const ax = state.currentAxes || { x: 0, y: 1 };
    state.cursorLeft = render2D(left, ax.x, ax.y);
  } else if (state.dim === 3) {
    const ax = state.currentAxes || { x: 0, y: 1, z: 2 };
    state.cursorLeft = render3D(left, ax.x, ax.y, ax.z);
  } else if (state.dim === 4) {
    const a = state.currentAxesA || { x: 0, y: 1 };
    const b = state.currentAxesB || { x: 2, y: 3 };
    state.cursorLeft  = render2D(left,  a.x, a.y);
    state.cursorRight = render2D(right, b.x, b.y);
  }

  // 4) assicura che Plotly ricalcoli le dimensioni dopo il cambio griglia
  queueMicrotask(() => {
    if (left)  Plotly.Plots.resize(left);
    if (state.dim === 4 && right) Plotly.Plots.resize(right);
  });
}


/* Aggiorna la posizione del cursore (in [0,1] → proiettato in u[-1,1]) */
export function updateCursor(latentPoint) {
  if (!latentPoint || latentPoint.length !== state.dim) return;
  const { left, right } = els();

  // helper per set 2D
  const restyle2D = (container, info, axX, axY) => {
    const x = latentToU(latentPoint[axX], axX, state.boundsMin, state.boundsMax);
    const y = latentToU(latentPoint[axY], axY, state.boundsMin, state.boundsMax);
    if (info && Number.isInteger(info.glowIdx)) {
      Plotly.restyle(container, { x: [[x]], y: [[y]] }, [info.glowIdx]);
      Plotly.restyle(container, { x: [[x]], y: [[y]] }, [info.dotIdx]);
    }
  };
  // helper per set 3D
  const restyle3D = (container, info, axX, axY, axZ) => {
    const x = latentToU(latentPoint[axX], axX, state.boundsMin, state.boundsMax);
    const y = latentToU(latentPoint[axY], axY, state.boundsMin, state.boundsMax);
    const z = latentToU(latentPoint[axZ], axZ, state.boundsMin, state.boundsMax);
    if (info && Number.isInteger(info.glowIdx)) {
      Plotly.restyle(container, { x: [[x]], y: [[y]], z: [[z]] }, [info.glowIdx]);
      Plotly.restyle(container, { x: [[x]], y: [[y]], z: [[z]] }, [info.dotIdx]);
    }
  };

  if (state.dim === 2) {
    const ax = state.currentAxes || { x: 0, y: 1 };
    restyle2D(left, state.cursorLeft, ax.x, ax.y);
  } else if (state.dim === 3) {
    const ax = state.currentAxes || { x: 0, y: 1, z: 2 };
    restyle3D(left, state.cursorLeft, ax.x, ax.y, ax.z);
  } else if (state.dim === 4) {
    const a = state.currentAxesA || { x: 0, y: 1 };
    const b = state.currentAxesB || { x: 2, y: 3 };
    restyle2D(left,  state.cursorLeft,  a.x, a.y);
    restyle2D(right, state.cursorRight, b.x, b.y);
  }
}
