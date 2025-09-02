# ==============================
# General / I/O / Logging
# ==============================
LOG_FOLDER = "./logs"
CHECKPOINTS_FOLDER = "./checkpoints"
CHECKPOINT_EXTENSION = ".pt"

# Random seeds for reproducibility
GLOBAL_SEED = 56


# ==============================
# Renderer params
# ==============================
NUM_CHANNELS = 2
SAMPLERATE = 48000
BLOCKSIZE = 1024
AUTOSAVE_INTERVAL = 5
TARGET_DBFS = -3.0
DATASET_FOLDER = "data"
RENDERED_AUDIO_FOLDER = "audio"
RECORDING_LENGTH = 2  # seconds


# ==============================
# Preprocess settings
# ==============================
BIAS_INIT = 1e-03
NOISE_MAGNITUDE = 2e-03
NOISE_FILTER = 0.3
DECIMAL_PLACES = 6
LOW_VARIANCE_THRESHOLD = 0.01
CORRELATION_THRESHOLD = 0.95
PCA_VARIANCE_THRESHOLD = 0.95


# ==============================
# Model / VAE defaults (added)
# ==============================
# Latent constraints used by assertions
MIN_LATENT_DIM = 2
MAX_LATENT_DIM = 4

# Normalised data range
DATA_MIN = 0.0
DATA_MAX = 1.0

# Visualization data range
VIS_MIN = -1.0
VIS_MAX = 1.0

# Loss/regularisation helpers
LOSS_EPSILON = 1e-8  # to prevent numerical instability
DEFAULT_KL_BETA = 0.0
DEFAULT_LEARNING_RATE = 1e-3
DEFAULT_INPUT_NOISE_STD = 0.0  # keep zero to maximise reconstruction

# Hidden dimension auto-layout fallbacks (used when hidden_dims is None)
HIDDEN_WIDTH_SCALE_DEFAULT = 1.0
HIDDEN_DEPTH_DEFAULT = 2
HIDDEN_ROUND_TO_DEFAULT = 8

# Training schedule
SEARCH_EPOCHS = 600
FINAL_EPOCHS = 4000

# Training loop control
PRUNE_ENABLED_DEFAULT = False
PRUNE_EVERY_EPOCHS = 50
BEST_IMPROVEMENT_EPS = 1e-10
DEFAULT_BATCH_SIZE = 0        # 0 => full-batch on tiny datasets
GRAD_CLIP_DEFAULT = 1.0
PER_FEATURE_WEIGHT_MIN = 1e-6

# Metrics
RECON_ACCURACY_THRESHOLD = 0.03  # 3% on [0,1]


# ==============================
# VAE hyperparameter search space
# ==============================
LATENT_EXPANSION_FACTOR = 8

VAE_PARAM_RANGES = {
    "learning_rate": {
        "type": "float",
        "low": 3e-4,
        "high": 3e-3,
        "log": True
    },
    "kl_beta": {
        "type": "float",
        "low": 1e-12,
        "high": 1e-7,
        "log": True
    },
    "latent_dim": {
        "type": "categorical",
        "values": [2, 3, 4]
    },
    "width_scale": {
        "type": "float",
        "low": 0.5,
        "high": 4.0,
        "log": False
    },
    "depth": {
        "type": "categorical",
        "values": [1, 2, 3]
    },
    "round_to": {
        "type": "categorical",
        "values": [8, 16, 32]
    },
    "grad_clip": {
        "type": "categorical",
        "values": [None, 0.5, 1.0, 2.0]
    }
}


# ==============================
# RBF hyperparameter search space
# ==============================
RBF_PARAM_RANGES = {
    "smoothing": {
        "type": "float",
        "low": 1e-12,
        "high": 1e-5,
        "log": True
    },
    "kernel": {
        "type": "categorical",
        "values": ["gaussian", "thin_plate_spline", "cubic", "inverse_quadratic", "linear"]
    },
    "epsilon_scale": {
        "type": "float",
        "low": 0.5,
        "high": 3.0,
        "log": False
    },
    "degree": {
        "type": "int",
        "low": -1,
        "high": 1,
        "log": False
    }
}

# Restrictions and kernel rules
RBF_MIN_DEGREE = {
    "linear": 0,
    "thin_plate_spline": 1,
    "cubic": 1
}

# Degree is forced to -1 (no polynomial queue)
RBF_DEGREE_LOCK = {
    "gaussian": -1,
    "inverse_quadratic": -1
}

# Kernels that ignore epsilon in SciPy
RBF_FIXED_EPSILON_KERNELS = ["linear", "thin_plate_spline", "cubic"]

# RBF evaluation helpers
RBF_OOB_PENALTY_WEIGHT = 30.0
RBF_OOB_PENALTY_POWER = 1.5
RBF_MEDIAN_DIST_FALLBACK = 1.0

# Latent normalisation default for RBF stage
NORMALISE_LATENT_DEFAULT = True


# ==============================
# Optimisation budget
# ==============================
N_TRIALS_VAE = 500
N_TRIALS_RBF = 300


# ==============================
# GUI / OSC
# ==============================
IP_ADDRESS = "127.0.0.1"
SEND_PORT = 9100
RECEIVE_PORT = 9101
FORWARD_PORT = 9110


# ==============================
# UX / Navigation
# ==============================
# Nearest-neighbour blending controls (post-RBF safety net)
# ---------------------------------------------------------
# NN_BLEND_SCALE:
#   Multiplier for the median nearest-neighbour distance.
#   Larger values (e.g. 2.0) make the blend activate later, only at the very edges;
#   smaller values (e.g. 1.2) make it activate earlier, even in denser regions.
#
# NN_BLEND_POWER:
#   Controls how sharply the blending weight decays with distance.
#   1 = gentle (soft fade), 2 = moderate (recommended default), 3 = steep (hard switch).
#
# Adjust these only if latent navigation feels unstable:
#   - Increase SCALE or POWER if you observe spikes near the borders.
#   - Decrease SCALE or POWER if the interpolation feels too "sticky" to the nearest point.

NN_BLEND_ENABLED_DEFAULT = True # Active by default to prevent spikes on latent space's borders
NN_BLEND_SCALE = 1.5
NN_BLEND_POWER = 2.0
NN_BLEND_ACTIVATION_THRESHOLD = 1e-12
