// net.js
/* global io */
import { state, latentToU, uToLatent } from "./core.js";

// Socket.IO client configured to use polling only (avoids WebSocket upgrade errors)
const socket = io({
  transports: ['polling']
});

// (Optional) expose for other modules/tools; harmless if unused
window.appSocket = socket;

/**
 * Send a cursor move originating from the UI (e.g., keyboard/mouse).
 * NOTE: this path is for user input; it already emits 'cursor_move' with { u, ... }.
 */
export function sendCursor(latentPoint) {
  const u = new Array(state.dim);
  for (let j = 0; j < state.dim; j++) u[j] = latentToU(latentPoint[j], j);
  state.localSeq += 1;
  socket.emit("cursor_move", { u, origin: state.inputSource, seq: state.localSeq });
}

/**
 * Wire browser-side listeners.
 * We:
 *  1) apply UI updates when the server broadcasts 'cursor_update'
 *  2) bounce the SAME vector 'u' back to the server as 'cursor_move'
 *     so that the server can forward param-by-param to ReaLearn.
 */
export function setupSocket(onCursorUpdate) {
  // Avoid duplicate handlers during hot-reload/dev
  socket.off("cursor_update");

  socket.on("cursor_update", (payload) => {
    try {
      const seq = (payload && typeof payload.seq === "number") ? payload.seq : null;

      // Guard against re-applying stale frames (idempotency)
      if (seq !== null && seq <= state.lastAppliedSeq) {
        if (payload && Array.isArray(payload.y)) {
          console.log("RBF reconstructed:", payload.y);
        }
        return;
      }

      // Expect the latent-space vector 'u' from server
      const u = payload && payload.u;
      if (!u || !Array.isArray(u)) return;
      if (u.length !== state.dim) return;

      // Convert u -> latent point for your UI and apply
      const lp = u.map((uu, i) => uToLatent(uu, i));
      onCursorUpdate(lp, payload);

      if (seq !== null) state.lastAppliedSeq = seq;

      if (payload && Array.isArray(payload.y)) {
        console.log("RBF reconstructed:", payload.y);
      }

      // ----------------------------------------------------------------------
      // Bounce back to the server to trigger socket_handlers.cursor_move
      // British English: we forward EXACTLY what we received (no normalisation).
      // This enables the server to send param-by-param to ReaLearn.
      // If you want a UI toggle (e.g., only when source === 'osc'), wrap this emit.
      // e.g., if (state.inputSource === 'osc') { ... }
      socket.emit("cursor_move", { cursor: u, origin: "osc" });
      // ----------------------------------------------------------------------
    } catch (err) {
      console.error("cursor_update error:", err);
    }
  });
}
