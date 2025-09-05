// /static/js/plot.js
/* global Plotly */
import { state, CONST, getColumn, latentToU } from "./core.js";

/* ---------- CSS helpers (single source of truth from CSS) ---------- */
function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}
function getSpikeColor() {
  return cssVar('--spike-color') || null;
}
function getPlotTextColor() {
  return cssVar('--plot-text') || null;
}

/* ---------- util DOM per i contenitori ---------- */
function els() {
  const grid  = document.getElementById("plots");
  const left  = document.getElementById("plot-left");
  const right = document.getElementById("plot-right");
  if (!grid)  throw new Error("#plots non trovato");
  if (!left)  throw new Error("#plot-left non trovato");
  if (!right) throw new Error("#plot-right non trovato");
  return { grid, left, right };
}

/* ---------- layout modes ---------- */
function setLayoutSingle({ bigMinHeightPx = 640 } = {}) {
  const { grid, left, right } = els();
  // 1 colonna: usiamo solo il sinistro e lo centriamo
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "1fr";
  grid.style.gap = "12px";

  left.style.display = "block";
  right.style.display = "none";
  left.style.minHeight = bigMinHeightPx + "px";
  left.style.margin = "0 auto"; // centra
}

function setLayoutDual({ smallMinHeightPx = 520 } = {}) {
  const { grid, left, right } = els();
  // 2 colonne affiancate
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "1fr 1fr";
  grid.style.gap = "12px";

  left.style.display = "block";
  right.style.display = "block";
  left.style.minHeight  = smallMinHeightPx + "px";
  right.style.minHeight = smallMinHeightPx + "px";
  left.style.margin  = "0";
  right.style.margin = "0";
}

// --- Applica i colori del tema CSS ai layout Plotly ---
function applyPlotTheme2D(layout){
  const r    = getComputedStyle(document.documentElement);
  const GRID = r.getPropertyValue('--plot-grid').trim();
  const AXIS = r.getPropertyValue('--plot-axis').trim();
  const TEXT = r.getPropertyValue('--plot-text').trim();

  layout.font = { ...(layout.font||{}), color: TEXT || layout.font?.color };

  layout.xaxis = {
    ...(layout.xaxis||{}),
    gridcolor: GRID || layout.xaxis?.gridcolor,
    linecolor: AXIS || layout.xaxis?.linecolor,
    tickfont: { color: TEXT },
    titlefont: { color: TEXT }
  };
  layout.yaxis = {
    ...(layout.yaxis||{}),
    gridcolor: GRID || layout.yaxis?.gridcolor,
    linecolor: AXIS || layout.yaxis?.linecolor,
    tickfont: { color: TEXT },
    titlefont: { color: TEXT }
  };
}

function applyPlotTheme3D(layout){
  const r    = getComputedStyle(document.documentElement);
  const GRID = r.getPropertyValue('--plot-grid').trim();
  const AXIS = r.getPropertyValue('--plot-axis').trim();
  const TEXT = r.getPropertyValue('--plot-text').trim();
  const BG   = r.getPropertyValue('--plot-bg').trim();

  layout.scene = layout.scene || {};
  layout.scene.bgcolor = BG || layout.scene.bgcolor;

  const patch = (ax) => ({
    ...(ax||{}),
    gridcolor: GRID || ax?.gridcolor,
    color:     AXIS || ax?.color,
    tickfont:  { color: TEXT },
    titlefont: { color: TEXT }
  });

  layout.scene.xaxis = patch(layout.scene.xaxis);
  layout.scene.yaxis = patch(layout.scene.yaxis);
  layout.scene.zaxis = patch(layout.scene.zaxis);
}


/* ---------- 2D ---------- */
function scatter2D(axX, axY, cursorPoint) {
  // Serie principali in u-space [-1,1]
  const x = getColumn(state.latent, axX).map(v => latentToU(v, axX));
  const y = getColumn(state.latent, axY).map(v => latentToU(v, axY));

  // Colore (scalar) da una dimensione extra se disponibile, altrimenti X
  const extras = Array.from({ length: state.dim }, (_, i) => i).filter(i => i !== axX && i !== axY);
  const colorDim = extras.length ? extras[0] : axX;
  const c = getColumn(state.latent, colorDim).map(v => latentToU(v, colorDim));

  // Etichette preset
  const labels = (state.presetNames && state.presetNames.length === x.length)
    ? state.presetNames
    : x.map((_, i) => `ID${i+1}`);

  // Posizione cursore (u-space)
  const cx_u = cursorPoint ? latentToU(cursorPoint[axX], axX) : 0;
  const cy_u = cursorPoint ? latentToU(cursorPoint[axY], axY) : 0;

  // Traccia punti (color coded)
  const pts = {
    type: "scattergl",
    mode: "markers",
    x, y,
    marker: { size: 7, color: c, colorscale: "Viridis", cmin: -1, cmax: 1, showscale: false },
    name: "presets",
  };

  // Testo etichette (SVG)
  const txt = {
    type: "scatter",
    mode: "text",
    x, y,
    text: labels,
    textposition: "top center",
    textfont: { size: 11, color: getPlotTextColor() || undefined },
    hoverinfo: "skip",
    showlegend: false,
  };

  // Cursore: glow + dot (usa i CONST del core.js per compatibilità)
  const glow = {
    type: "scattergl",
    mode: "markers",
    x: [cx_u], y: [cy_u],
    marker: { size: CONST.CURSOR_GLOW_SIZE, opacity: CONST.CURSOR_GLOW_OPACITY, color: CONST.CURSOR_GLOW_COLOR },
    hoverinfo: "skip", showlegend: false,
  };
  const dot = {
    type: "scattergl",
    mode: "markers",
    x: [cx_u], y: [cy_u],
    marker: { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: { color: CONST.CURSOR_DOT_LINE, width: 1 } },
    hoverinfo: "skip", showlegend: false,
  };

  const SPIKE = getSpikeColor();
  const layout = {
    xaxis: {
      title: state.axisNames[axX],
      range: [-1, 1],
      ...(SPIKE ? { spikecolor: SPIKE } : {}),
    },
    yaxis: {
      title: state.axisNames[axY],
      range: [-1, 1],
      ...(SPIKE ? { spikecolor: SPIKE } : {}),
    },
    margin: { t: 10, r: 10, b: 40, l: 40 },
    paper_bgcolor: CONST.BG_COLOR, plot_bgcolor: CONST.BG_COLOR,
    uirevision: "static",
  };

  applyPlotTheme2D(layout);

  return { traces: [pts, txt, glow, dot], layout, glowIdx: 2, dotIdx: 3 };
}

/* ---------- 3D ---------- */
function scatter3D(axX, axY, axZ, cursorPoint) {
  // Dati in u-space
  const x = getColumn(state.latent, axX).map(v => latentToU(v, axX));
  const y = getColumn(state.latent, axY).map(v => latentToU(v, axY));
  const z = getColumn(state.latent, axZ).map(v => latentToU(v, axZ));

  // Etichette preset
  const N = x.length;
  const labels = (state.presetNames && state.presetNames.length === N)
    ? state.presetNames
    : Array.from({ length: N }, (_, i) => `ID${i + 1}`);

  // Cursore (u-space)
  const cx_u = cursorPoint ? latentToU(cursorPoint[axX], axX) : 0;
  const cy_u = cursorPoint ? latentToU(cursorPoint[axY], axY) : 0;
  const cz_u = cursorPoint ? latentToU(cursorPoint[axZ], axZ) : 0;

  // Punti 3D (color coded su z)
  const pts = {
    type: "scatter3d",
    mode: "markers",
    x, y, z,
    marker: {
      size: 4.5,
      color: z,
      colorscale: "Viridis",
      cmin: -1, cmax: 1,
      showscale: false
    },
    name: "presets",
  };

  // Etichette 3D
  const txt3d = {
    type: "scatter3d",
    mode: "text",
    x, y, z,
    text: labels,
    textposition: "top center",
    textfont: { size: 11, color: getPlotTextColor() || undefined },
    hoverinfo: "skip",
    showlegend: false,
  };

  // Cursore 3D
  const glow = {
    type: "scatter3d",
    mode: "markers",
    x: [cx_u], y: [cy_u], z: [cz_u],
    marker: { size: CONST.CURSOR_GLOW_SIZE, opacity: CONST.CURSOR_GLOW_OPACITY, color: CONST.CURSOR_GLOW_COLOR },
    hoverinfo: "skip", showlegend: false,
  };
  const dot = {
    type: "scatter3d",
    mode: "markers",
    x: [cx_u], y: [cy_u], z: [cz_u],
    marker: { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: { color: CONST.CURSOR_DOT_LINE, width: 1 } },
    hoverinfo: "skip", showlegend: false,
  };

  const SPIKE = getSpikeColor();
  const layout = {
    scene: {
      xaxis: { title: state.axisNames[axX], range: [-1, 1], ...(SPIKE ? { spikecolor: SPIKE } : {}) },
      yaxis: { title: state.axisNames[axY], range: [-1, 1], ...(SPIKE ? { spikecolor: SPIKE } : {}) },
      zaxis: { title: state.axisNames[axZ], range: [-1, 1], ...(SPIKE ? { spikecolor: SPIKE } : {}) },
      bgcolor: CONST.BG_COLOR,
      uirevision: "static",
      ...(state.lastCamera ? { camera: state.lastCamera } : {}),
    },
    margin: { t: 10, r: 10, b: 10, l: 10 },
    paper_bgcolor: CONST.BG_COLOR,
  };

  applyPlotTheme3D(layout);

  return { traces: [pts, txt3d, glow, dot], layout, glowIdx: 2, dotIdx: 3 };
}

/* ---------- API esportate ---------- */
export function drawPlots() {
  const { left, right } = els();

  if (state.dim === 2) {
    // singolo grafico grande
    setLayoutSingle({ bigMinHeightPx: 640 });
    const { traces, layout, glowIdx, dotIdx } =
      scatter2D(state.currentAxes.x, state.currentAxes.y, state.cursorPoint);
    Plotly.react(left, traces, layout, { responsive: true });
    state.is3D = false;
    state.cursorLeft = { glowIdx, dotIdx };
    state.cursorRight = null;
    return;
  }

  if (state.dim === 3) {
    // singolo grafico 3D grande
    setLayoutSingle({ bigMinHeightPx: 640 });
    const { traces, layout, glowIdx, dotIdx } =
      scatter3D(state.currentAxes.x, state.currentAxes.y, state.currentAxes.z, state.cursorPoint);
    Plotly.react(left, traces, layout, { responsive: true });
    state.is3D = true;
    state.cursorLeft = { glowIdx, dotIdx };
    state.cursorRight = null;

    // salva camera per persistenza tra redraw
    left.on('plotly_relayout', (ev) => {
      if (ev && (ev['scene.camera'] || ev['scene.camera.eye'] || ev['scene.camera.center'] || ev['scene.camera.up'])) {
        const gd = left;
        const sc = gd._fullLayout && gd._fullLayout.scene && gd._fullLayout.scene._scene && gd._fullLayout.scene._scene.getCamera && gd._fullLayout.scene._scene.getCamera();
        if (sc && sc.eye) {
          state.lastCamera = sc;
        }
      }
    });
    return;
  }

  // 4D: due viste 2D affiancate
  setLayoutDual({ smallMinHeightPx: 520 });

  const a = state.currentAxesA || { x: 0, y: 1 };
  const b = state.currentAxesB || { x: 2, y: 3 };

  const A = scatter2D(a.x, a.y, state.cursorPoint);
  Plotly.react(left, A.traces, A.layout, { responsive: true });
  state.cursorLeft = { glowIdx: A.glowIdx, dotIdx: A.dotIdx };

  const B = scatter2D(b.x, b.y, state.cursorPoint);
  Plotly.react(right, B.traces, B.layout, { responsive: true });
  state.cursorRight = { glowIdx: B.glowIdx, dotIdx: B.dotIdx };

  state.is3D = false; // entrambe viste 2D
}

export function updateCursor(latentPoint) {
  const { left, right } = els();
  if (!latentPoint || latentPoint.length !== state.dim) return;

  if (state.dim === 2) {
    const axX = Number(state.currentAxes.x);
    const axY = Number(state.currentAxes.y);
    const cx_u = latentToU(latentPoint[axX], axX);
    const cy_u = latentToU(latentPoint[axY], axY);
    if (state.cursorLeft) {
      Plotly.restyle(left, { x: [[cx_u]], y: [[cy_u]] }, [state.cursorLeft.glowIdx]);
      Plotly.restyle(left, { x: [[cx_u]], y: [[cy_u]] }, [state.cursorLeft.dotIdx]);
    }
    return;
  }

  if (state.dim === 3) {
    const axX = Number(state.currentAxes.x);
    const axY = Number(state.currentAxes.y);
    const axZ = Number(state.currentAxes.z);
    const cx_u = latentToU(latentPoint[axX], axX);
    const cy_u = latentToU(latentPoint[axY], axY);
    const cz_u = latentToU(latentPoint[axZ], axZ);
    if (state.cursorLeft) {
      Plotly.restyle(left, { x: [[cx_u]], y: [[cy_u]], z: [[cz_u]] }, [state.cursorLeft.glowIdx]);
      Plotly.restyle(left, { x: [[cx_u]], y: [[cy_u]], z: [[cz_u]] }, [state.cursorLeft.dotIdx]);
    }
    return;
  }

  // 4D: due viste 2D
  const a = state.currentAxesA || { x: 0, y: 1 };
  const b = state.currentAxesB || { x: 2, y: 3 };
  const ax_u = latentToU(latentPoint[a.x], a.x);
  const ay_u = latentToU(latentPoint[a.y], a.y);
  const bx_u = latentToU(latentPoint[b.x], b.x);
  const by_u = latentToU(latentPoint[b.y], b.y);

  if (state.cursorLeft) {
    Plotly.restyle(left,  { x: [[ax_u]], y: [[ay_u]] }, [state.cursorLeft.glowIdx]);
    Plotly.restyle(left,  { x: [[ax_u]], y: [[ay_u]] }, [state.cursorLeft.dotIdx]);
  }
  if (state.cursorRight) {
    Plotly.restyle(right, { x: [[bx_u]], y: [[by_u]] }, [state.cursorRight.glowIdx]);
    Plotly.restyle(right, { x: [[bx_u]], y: [[by_u]] }, [state.cursorRight.dotIdx]);
  }
}

