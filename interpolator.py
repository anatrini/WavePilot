from typing import Sequence

import numpy as np
from scipy.interpolate import RBFInterpolator

from constants import RBF_FIXED_EPSILON_KERNELS  # kernels that ignore epsilon
from logger import setup_logger

logging = setup_logger("Radial Basis Function Interpolator")


class RBFInterpolation:
    """
    Thin wrapper around SciPy's RBFInterpolator that:
      - is latent-dimensionality agnostic (works for d = 2..n),
      - maps UI cursor positions u ∈ [-1, 1]^k to the latent fitting space actually used to train
        the RBF (either the raw latent or the z-scored latent),
      - exposes a stable API for sending interpolated data via OSC.

    Parameters
    ----------
    reduced_data : np.ndarray of shape (N, d)
        Latent coordinates used to fit the RBF. They must already be in the fitting space you intend to use (e.g., externally z-scored).
    original_data : np.ndarray of shape (N, D)
        Target data in [0, 1] (normalised) to be reconstructed via interpolation from latent space.
    smoothing : float
        RBF smoothing parameter (small ≈ interpolation; larger ≈ regression).
    kernel : str
        RBF kernel name as per SciPy.
    epsilon : float
        RBF epsilon (shape parameter). For kernels in `RBF_FIXED_EPSILON_KERNELS`, SciPy ignores it.
    degree : int
        Polynomial degree (-1: none, 0: constant, 1: linear). Honour upstream rules/constraints.
    """

    def __init__(
        self,
        reduced_data: np.ndarray,
        original_data: np.ndarray,
        smoothing: float,
        kernel: str,
        epsilon: float,
        *,
        degree: int
    ):
        # Store core hyperparameters
        self.kernel = kernel
        self.smoothing = float(smoothing)
        self.degree = int(degree)
        self.epsilon = float(epsilon)

        # Validate and store latent/targets
        Z = np.asarray(reduced_data, dtype=np.float64)
        Y = np.asarray(original_data, dtype=np.float64)
        assert Z.ndim == 2, "reduced_data must be 2D of shape [N, d]."
        assert Y.ndim == 2, "original_data must be 2D of shape [N, D]."
        assert Z.shape[0] == Y.shape[0], "Latent and target data must have the same number of samples."
        self.latent_dim = int(Z.shape[1])

        # Per-dimension latent bounds in the *fitting* space
        self.bounds_min = Z.min(axis=0)
        self.bounds_max = Z.max(axis=0)

        # Epsilon note: for certain kernels SciPy ignores epsilon; no special handling required.
        if self.kernel in RBF_FIXED_EPSILON_KERNELS:
            logging.debug("Kernel %s ignores epsilon; value provided will be disregarded by SciPy.", self.kernel)

        # Fit the interpolator in the exact space in which we will query it
        self.interpolator = RBFInterpolator(
            Z,
            Y,
            smoothing=self.smoothing,
            kernel=self.kernel,
            epsilon=self.epsilon,
            degree=self.degree,
        )

    # ------------------- internal helpers -------------------

    def _scale_coord(self, u_val: float, dim: int) -> float:
        """
        Map a single cursor coordinate u ∈ [-1, 1] to the dim-th latent coordinate in the fitting
        space using the pre-computed per-dimension bounds.
        """
        return (u_val + 1.0) * 0.5 * (self.bounds_max[dim] - self.bounds_min[dim]) + self.bounds_min[dim]

    def _to_latent_from_cursor(self, cursor_position: Sequence[float]) -> np.ndarray:
        """
        Map a cursor position u ∈ [-1, 1]^k to a latent vector x ∈ ℝ^d in the fitting space. Requirement: k must equal d.
        """
        u = np.asarray(cursor_position, dtype=np.float64).reshape(-1)
        k = int(u.shape[0])
        d = self.latent_dim

        if k != d:
            raise ValueError(
                "Cursor dimensionality is %s but latent dimensionality is %s." % (k, d)
            )
        
        x = np.empty(d, dtype=np.float64)
        for j in range(d):
            x[j] = self._scale_coord(u[j], j)

        return x.reshape(1, -1)

    # ------------------- public API -------------------

    def denormalize(self, cursor_position: Sequence[float]) -> Sequence[float]:
        """
        Map a UI cursor position u ∈ [-1, 1]^k to the corresponding coordinates in the latent
        fitting space (raw or z-scored), using the same bounds and axis mapping used at fit time.

        Returns
        -------
        list[float]
            A list of length d (latent dimensionality) with the latent coordinates in the fitting space.
        """
        return self._to_latent_from_cursor(cursor_position).ravel().tolist()

    def interpolate(self, cursor_position: Sequence[float]) -> np.ndarray:
        """
        Convert a UI cursor position u ∈ [-1, 1]^k into the fitting latent space and query the RBF.
        The output is clipped to [0, 1] for downstream safety.
        """
        x = self._to_latent_from_cursor(cursor_position)
        y = self.interpolator(x)
        return np.clip(y, 0.0, 1.0)

    def send_data(self, osc_client, cursor_position: Sequence[float]) -> None:
        """
        Interpolate at the given cursor position and send the flat list via OSC under
        the address '/interpolated_data'.
        """
        interpolated_data = self.interpolate(cursor_position)
        # logging.info("Interpolated data length: %s", interpolated_data.size)
        osc_client.send_message("/interpolated_data", interpolated_data.flatten().tolist())
