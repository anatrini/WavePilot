// /static/js/plot.js
/* global Plotly */
import { state, CONST, getColumn, latentToU } from "./core.js";

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
  const x = getColumn(state.latent, axX).map(v => latentToU(v, axX));
  const y = getColumn(state.latent, axY).map(v => latentToU(v, axY));

  const extras = Array.from({ length: state.dim }, (_, i) => i).filter(i => i !== axX && i !== axY);
  const colorDim = extras.length ? extras[0] : axX;

  const c = getColumn(state.latent, colorDim).map(v => latentToU(v, colorDim));

  const cx_u = cursorPoint ? latentToU(cursorPoint[axX], axX) : 0;
  const cy_u = cursorPoint ? latentToU(cursorPoint[axY], axY) : 0;


  const pts = {
    type: "scattergl",
    mode: "markers",
    x, y,
    marker: { 
        size: 5, 
        color: c,
        colorscale: "Viridis",
        cmin: -1,
        cmax: 1,
        showscale: false
    },
    name: "anchors",
  };

  const glow = {
    type: "scattergl",
    mode: "markers",
    x: [cx_u], y: [cy_u],
    marker: { 
        size: CONST.CURSOR_GLOW_SIZE, 
        opacity: CONST.CURSOR_GLOW_OPACITY, 
        color: CONST.CURSOR_GLOW_COLOR 
    },
    hoverinfo: "skip",
    showlegend: false,
  };

  const dot = {
    type: "scattergl",
    mode: "markers",
    x: [cx_u], y: [cy_u],
    marker: { 
        size: CONST.CURSOR_DOT_SIZE, 
        color: CONST.CURSOR_DOT_COLOR, 
        line: { 
            width: 2, 
            color: CONST.CURSOR_DOT_LINE 
        } 
    },
    hoverinfo: "skip",
    showlegend: false,
  };

  const layout = {
    dragmode: "pan",
    hovermode: "closest",
    xaxis: { title: state.axisNames[axX], range: [-1, 1] },
    yaxis: { title: state.axisNames[axY], range: [-1, 1] },
    margin: { t: 10, r: 10, b: 40, l: 40 },
    paper_bgcolor: CONST.BG_COLOR,
    plot_bgcolor: CONST.BG_COLOR,
    uirevision: "static",
  };

  return { traces: [pts, glow, dot], layout, glowIdx: 1, dotIdx: 2 };
}

function scatter3D(axX, axY, axZ, cursorPoint) {
  const x = getColumn(state.latent, axX).map(v => latentToU(v, axX));
  const y = getColumn(state.latent, axY).map(v => latentToU(v, axY));
  const z = getColumn(state.latent, axZ).map(v => latentToU(v, axZ));

  const cx_u = cursorPoint ? latentToU(cursorPoint[axX], axX) : 0;
  const cy_u = cursorPoint ? latentToU(cursorPoint[axY], axY) : 0;
  const cz_u = cursorPoint ? latentToU(cursorPoint[axZ], axZ) : 0;

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
    x: [cx_u], y: [cy_u], z: [cz_u],
    marker: { size: CONST.CURSOR_GLOW_SIZE, opacity: CONST.CURSOR_GLOW_OPACITY, color: CONST.CURSOR_GLOW_COLOR },
    hoverinfo: "skip",
    showlegend: false,
  };
  const dot = {
    type: "scatter3d",
    mode: "markers",
    x: [cx_u], y: [cy_u], z: [cz_u],
    marker: { size: CONST.CURSOR_DOT_SIZE, color: CONST.CURSOR_DOT_COLOR, line: { width: 2, color: CONST.CURSOR_DOT_LINE } },
    hoverinfo: "skip",
    showlegend: false,
  };

  const layout = {
    scene: {
      xaxis: { title: state.axisNames[axX], range: [-1, 1] },
      yaxis: { title: state.axisNames[axY], range: [-1, 1] },
      zaxis: { title: state.axisNames[axZ], range: [-1, 1] },
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
    // assi correnti (forziamo Number nel dubbio arrivino stringhe dai <select>)
    const axX = Number(state.currentAxes.x);
    const axY = Number(state.currentAxes.y);

    // latentPoint è in [0,1] -> converti in u-space [-1,1] per disegnare
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

  // dim === 4 → due viste 2D
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

