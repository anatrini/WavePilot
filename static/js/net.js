// net.js
/* global io */
import { state, latentToU, uToLatent } from "./core.js";

const socket = io();

export function sendCursor(latentPoint) {
  const u = new Array(state.dim);
  for (let j = 0; j < state.dim; j++) u[j] = latentToU(latentPoint[j], j);
  state.localSeq += 1;
  socket.emit("cursor_move", { u, origin: state.inputSource, seq: state.localSeq });
}

export function setupSocket(onCursorUpdate) {
  socket.on("cursor_update", (payload) => {
    try {
      const seq = (payload && typeof payload.seq === "number") ? payload.seq : null;
      if (seq !== null && seq <= state.lastAppliedSeq) {
        if (payload && Array.isArray(payload.y)) {
          console.log("RBF reconstructed:", payload.y);
        }
        return;
      }
      const u = payload && payload.u;
      if (!u || !Array.isArray(u)) return;
      if (u.length !== state.dim) return;

      const lp = u.map((uu, i) => uToLatent(uu, i));
      onCursorUpdate(lp, payload);

      if (seq !== null) state.lastAppliedSeq = seq;

      if (payload && Array.isArray(payload.y)) {
        console.log("RBF reconstructed:", payload.y);
      }
    } catch (err) {
      console.error("cursor_update error:", err);
    }
  });
}
