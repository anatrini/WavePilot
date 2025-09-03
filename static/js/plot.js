// plot.js
/* global Plotly */
import { state, CONST, getColumn } from "./core.js";
import { dom } from "./ui.js";

export function makeScatterTraces() {
  const axX = state.currentAxes.x;
  const axY = state.currentAxes.y;
  const axZ = state.currentAxes.z;

  const x = getColumn(state.latent, axX);
  const y = getColumn(state.latent, axY);

  const cx = (state.cursorPoint && state.cursorPoint.length)
    ? state.cursorPoint[axX]
    : 0.5 * (state.boundsMin[axX] + state.boundsMax[axX]);
  const cy = (state.cursorPoint && state.cursorPoint.length)
    ? state.cursorPoint[axY]
    : 0.5 * (state.boundsMin[axY] + state.boundsMax[axY]);
  const cz = (typeof axZ === "number" && state.cursorPoint && state.cursorPoint.length)
    ? state.cursorPoint[axZ]
    : 0.0;

  const traces = [];
  let layout;
  let is3DLocal = false;

  if (state.dim === 2) {
    const pts2d = {
      type: "scattergl",
      mode: "markers",
      x, y,
      marker: {
        size: 3,
        color: CONST.MARKER_COLOR
      },
      name: "anchors"
    };

    const cursorGlow2d = {
      type: "scattergl",
      mode: "markers",
      x: [cx], y: [cy],
      marker: {
        size: CONST.CURSOR_GLOW_SIZE,
        opacity: CONST.CURSOR_GLOW_OPACITY,
        color: CONST.CURSOR_GLOW_COLOR
      },
      hoverinfo: "skip",
      showlegend: false
    };

    const cursorDot2d = {
      type: "scattergl",
      mode: "markers",
      x: [cx], y: [cy],
      marker: {
        size: CONST.CURSOR_DOT_SIZE,
        color: CONST.CURSOR_DOT_COLOR,
        line: { width: 2, color: CONST.CURSOR_DOT_LINE },
        symbol: "circle"
      },
      hoverinfo: "skip",
      showlegend: false
    };

    traces.push(pts2d, cursorGlow2d, cursorDot2d);

    layout = {
      dragmode: "pan",
      hovermode: "closest",
      xaxis: { title: state.axisNames[axX] },
      yaxis: { title: state.axisNames[axY] },
      margin: { t: 10, r: 10, b: 40, l: 40 },
      paper_bgcolor: CONST.BG_COLOR,
      plot_bgcolor: CONST.BG_COLOR,
      uirevision: "static"
    };

    return {
      traces,
      layout,
      is3D: false,
      cursorIndices: { glow: traces.length - 2, dot: traces.length - 1 }
    };
  }

  const z = getColumn(state.latent, axZ);

  if (state.dim === 4 && state.sliceDim != null) {
    const HALF_W = 0.12;
    const near = { x: [], y: [], z: [] };
    const far  = { x: [], y: [], z: [] };

    for (let i = 0; i < state.latent.length; i++) {
      const wVal = state.latent[i][state.sliceDim];
      const tgt = (Math.abs(wVal - state.sliceW0) <= HALF_W) ? near : far;
      tgt.x.push(x[i]); tgt.y.push(y[i]); tgt.z.push(z[i]);
    }

    traces.push({
      type: "scatter3d",
      mode: "markers",
      x: near.x, y: near.y, z: near.z,
      marker: {
        size: 3,
        color: near.z.length === z.length ? z : near.z,
        colorscale: "Viridis",
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
        colorscale: "Viridis",
        showscale: false,
        opacity: 0.10
      },
      name: "anchors (off-slice)"
    });
  } else {
    traces.push({
      type: "scatter3d",
      mode: "markers",
      x, y, z,
      marker: {
        size: 3,
        color: z,                 // depth cue
        colorscale: "Viridis",
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
      size: CONST.CURSOR_GLOW_SIZE,
      opacity: CONST.CURSOR_GLOW_OPACITY,
      color: CONST.CURSOR_GLOW_COLOR
    },
    hoverinfo: "skip",
    showlegend: false
  };

  const cursorDot3d = {
    type: "scatter3d",
    mode: "markers",
    x: [cx], y: [cy], z: [cz],
    marker: {
      size: CONST.CURSOR_DOT_SIZE,
      color: CONST.CURSOR_DOT_COLOR,
      line: { width: 2, color: CONST.CURSOR_DOT_LINE },
      symbol: "circle"
    },
    hoverinfo: "skip",
    showlegend: false
  };

  traces.push(cursorGlow3d, cursorDot3d);

  layout = {
    scene: {
      xaxis: { title: state.axisNames[axX] },
      yaxis: { title: state.axisNames[axY] },
      zaxis: { title: state.axisNames[axZ] },
      bgcolor: CONST.BG_COLOR,
      uirevision: "static",
      ...(state.lastCamera ? { camera: state.lastCamera } : {})
    },
    margin: { t: 10, r: 10, b: 10, l: 10 },
    paper_bgcolor: CONST.BG_COLOR
  };

  return {
    traces,
    layout,
    is3D: true,
    cursorIndices: { glow: traces.length - 2, dot: traces.length - 1 }
  };
}

export function drawPlot() {
  const { traces, layout, cursorIndices, is3D } = makeScatterTraces();
  Plotly.react(dom.plotEl, traces, layout, { responsive: true });
  state.cursorGlowIdx = cursorIndices.glow;
  state.cursorDotIdx  = cursorIndices.dot;
  state.is3D = !!is3D;
}

export function updateCursor(latentPoint) {
  if (!latentPoint || !Array.isArray(latentPoint) || latentPoint.length !== state.dim) return;

  const cx = latentPoint[state.currentAxes.x];
  const cy = latentPoint[state.currentAxes.y];

  if (!state.is3D) {
    if (state.cursorGlowIdx >= 0) {
      Plotly.restyle(dom.plotEl, { x: [[cx]], y: [[cy]] }, [state.cursorGlowIdx]);
    }
    if (state.cursorDotIdx >= 0) {
      Plotly.restyle(dom.plotEl, { x: [[cx]], y: [[cy]] }, [state.cursorDotIdx]);
    }
    return;
  }

  const cz = (typeof state.currentAxes.z === "number") ? latentPoint[state.currentAxes.z] : 0.0;

  if (state.cursorGlowIdx >= 0) {
    Plotly.restyle(dom.plotEl, { x: [[cx]], y: [[cy]], z: [[cz]] }, [state.cursorGlowIdx]);
  }
  if (state.cursorDotIdx >= 0) {
    Plotly.restyle(dom.plotEl, { x: [[cx]], y: [[cy]], z: [[cz]] }, [state.cursorDotIdx]);
  }
}

export function applySliceFromLatent(latentPoint) {
  if (state.dim !== 4) return;
  state.sliceW0 = latentPoint[state.sliceDim];
  if (dom.wSlider && dom.wReadout) {
    // reuse latentToU indirectly through bounds: compute normalised u manually
    const lo = state.boundsMin[state.sliceDim], hi = state.boundsMax[state.sliceDim];
    const denom = Math.max(1e-12, (hi - lo));
    const u = 2.0 * (state.sliceW0 - lo) / denom - 1.0;
    state.wValue = Math.max(-1, Math.min(1, u));
    dom.wSlider.value = String(state.wValue);
    dom.wReadout.textContent = state.wValue.toFixed(2);
  }
  drawPlot();
  updateCursor(latentPoint);
}
