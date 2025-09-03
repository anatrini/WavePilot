// /static/js/plot.js
/* global Plotly */
import { state, CONST, getColumn } from "./core.js";

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
  // 1 colonna, sinistro centrato e grande
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "1fr";
  grid.style.gap = "12px";

  right.style.display = "none";        // nascondi completamente il destro
  Plotly.purge(right);                  // libera eventuale grafico precedente

  left.style.display = "block";
  left.style.minHeight = bigMinHeightPx + "px";
  left.style.margin = "0 auto";         // centra orizzontalmente
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

/* ---------- tracce 2D / 3D ---------- */
function scatter2D(axX, axY, cursorPoint) {
  const x = getColumn(state.latent, axX);
  const y = getColumn(state.latent, axY);

  const cx = cursorPoint ? cursorPoint[axX] : 0.5 * (state.boundsMin[axX] + state.boundsMax[axX]);
  const cy = cursorPoint ? cursorPoint[axY] : 0.5 * (state.boundsMin[axY] + state.boundsMax[axY]);

  const pts = {
    type: "scattergl",
    mode: "markers",
    x, y,
    marker: { size: 3, color: CONST.MARKER_COLOR },
    name: "anchors",
  };
  const glow = {
    type: "scattergl",
    mode: "markers",
    x: [cx], y: [cy],
    marker: { size: CONST.CURSOR_GLOW_SIZE, opacity: CONST.CURSOR_GLOW_OPACITY, color: CONST.CURSOR_GLOW_COLOR },
    hoverinfo: "skip",
    showlegend: false,
  };
  const dot = {
    type: "scattergl",
    mode: "markers",
    x: [cx], y: [cy],
    marker: { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: { width: 2, color: CONST.CURSOR_DOT_LINE } },
    hoverinfo: "skip",
    showlegend: false,
  };

  const layout = {
    dragmode: "pan",
    hovermode: "closest",
    xaxis: { title: state.axisNames[axX] },
    yaxis: { title: state.axisNames[axY] },
    margin: { t: 10, r: 10, b: 40, l: 40 },
    paper_bgcolor: CONST.BG_COLOR,
    plot_bgcolor: CONST.BG_COLOR,
    uirevision: "static",
  };

  return { traces: [pts, glow, dot], layout, glowIdx: 1, dotIdx: 2 };
}

function scatter3D(axX, axY, axZ, cursorPoint) {
  const x = getColumn(state.latent, axX);
  const y = getColumn(state.latent, axY);
  const z = getColumn(state.latent, axZ);

  const cx = cursorPoint ? cursorPoint[axX] : 0.5 * (state.boundsMin[axX] + state.boundsMax[axX]);
  const cy = cursorPoint ? cursorPoint[axY] : 0.5 * (state.boundsMin[axY] + state.boundsMax[axY]);
  const cz = cursorPoint ? cursorPoint[axZ] : 0.5 * (state.boundsMin[axZ] + state.boundsMax[axZ]);

  const pts = {
    type: "scatter3d",
    mode: "markers",
    x, y, z,
    marker: { size: 3, color: z, colorscale: "Viridis", showscale: false },
    name: "anchors",
  };
  const glow = {
    type: "scatter3d",
    mode: "markers",
    x: [cx], y: [cy], z: [cz],
    marker: { size: CONST.CURSOR_GLOW_SIZE, opacity: CONST.CURSOR_GLOW_OPACITY, color: CONST.CURSOR_GLOW_COLOR },
    hoverinfo: "skip",
    showlegend: false,
  };
  const dot = {
    type: "scatter3d",
    mode: "markers",
    x: [cx], y: [cy], z: [cz],
    marker: { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: { width: 2, color: CONST.CURSOR_DOT_LINE } },
    hoverinfo: "skip",
    showlegend: false,
  };

  const layout = {
    scene: {
      xaxis: { title: state.axisNames[axX] },
      yaxis: { title: state.axisNames[axY] },
      zaxis: { title: state.axisNames[axZ] },
      bgcolor: CONST.BG_COLOR,
      uirevision: "static",
      ...(state.lastCamera ? { camera: state.lastCamera } : {}),
    },
    margin: { t: 10, r: 10, b: 10, l: 10 },
    paper_bgcolor: CONST.BG_COLOR,
  };

  return { traces: [pts, glow, dot], layout, glowIdx: 1, dotIdx: 2 };
}

/* ---------- API esportate ---------- */
export function drawPlots() {
  const { left, right } = els();

  if (state.dim === 2) {
    // layout: singolo grande centrato
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
    // layout: singolo grande centrato
    setLayoutSingle({ bigMinHeightPx: 640 });
    const { traces, layout, glowIdx, dotIdx } =
      scatter3D(state.currentAxes.x, state.currentAxes.y, state.currentAxes.z, state.cursorPoint);
    Plotly.react(left, traces, layout, { responsive: true });
    state.is3D = true;
    state.cursorLeft = { glowIdx, dotIdx };
    state.cursorRight = null;
    return;
  }

  // dim === 4 → due grafici affiancati (più piccoli)
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
    const axX = state.currentAxes.x, axY = state.currentAxes.y;
    const cx = latentPoint[axX], cy = latentPoint[axY];
    if (state.cursorLeft) {
      Plotly.restyle(left, { x: [[cx]], y: [[cy]] }, [state.cursorLeft.glowIdx]);
      Plotly.restyle(left, { x: [[cx]], y: [[cy]] }, [state.cursorLeft.dotIdx]);
    }
    return;
  }

  if (state.dim === 3) {
    const axX = state.currentAxes.x, axY = state.currentAxes.y, axZ = state.currentAxes.z;
    const cx = latentPoint[axX], cy = latentPoint[axY], cz = latentPoint[axZ];
    if (state.cursorLeft) {
      Plotly.restyle(left, { x: [[cx]], y: [[cy]], z: [[cz]] }, [state.cursorLeft.glowIdx]);
      Plotly.restyle(left, { x: [[cx]], y: [[cy]], z: [[cz]] }, [state.cursorLeft.dotIdx]);
    }
    return;
  }

  // 4D dual 2D
  const a = state.currentAxesA || { x: 0, y: 1 };
  const b = state.currentAxesB || { x: 2, y: 3 };

  const cax = latentPoint[a.x], cay = latentPoint[a.y];
  if (state.cursorLeft) {
    Plotly.restyle(left, { x: [[cax]], y: [[cay]] }, [state.cursorLeft.glowIdx]);
    Plotly.restyle(left, { x: [[cax]], y: [[cay]] }, [state.cursorLeft.dotIdx]);
  }

  const cbx = latentPoint[b.x], cby = latentPoint[b.y];
  if (state.cursorRight) {
    Plotly.restyle(right, { x: [[cbx]], y: [[cby]] }, [state.cursorRight.glowIdx]);
    Plotly.restyle(right, { x: [[cbx]], y: [[cby]] }, [state.cursorRight.dotIdx]);
  }
}
