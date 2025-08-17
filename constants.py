# Renderer params
NUM_CHANNELS = 2
SAMPLERATE = 48000
BLOCKSIZE = 1024
AUTOSAVE_INTERVAL = 5
TARGET_DBFS = -3.0
DATASET_FOLDER = "data"
RENDERED_AUDIO_FOLDER = "audio"
RECORDING_LENGTH = 2 # recording length in seconds

# Preprocess settings
BIAS_INIT = 1e-03
NOISE_MAGNITUDE = 2e-03
NOISE_FILTER = 0.3
DECIMAL_PLACES = 6
LOW_VARIANCE_THRESHOLD = 0.01
CORRELATION_THRESHOLD = 0.95
PCA_VARIANCE_THRESHOLD = 0.95

LOG_FOLDER = "./logs"

#LATENT_SPACE_SIZE = 3 # overwritten by latent_dim
#TORCH_MANUAL_SEED = 12

# Random seeds for reproducibility
GLOBAL_SEED = 56

# VAE parameter ranges, structured by type
LATENT_EXPANSION_FACTOR = 8
LOSS_EPSILON = 1e-8 # to prevent numerical instability

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
    "max_epochs": {
        "type": "categorical",
        "values": [2000, 5000]
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

# RBF parameter ranges, structured by type
RBF_PARAM_RANGES = {
    "smoothing": {
        "type": "float",
        "low": 1e-8,
        "high": 1e-2,
        "log": True
    },
    "kernel": {
        "type": "categorical",
        "values": ["gaussian","thin_plate_spline", "cubic", "inverse_quadratic", "linear"]
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

RBF_FIXED_EPSILON_KERNELS = ["linear", "thin_plate_spline", "cubic"]


# Number of trials for optimization
N_TRIALS_VAE = 500
N_TRIALS_RBF = 300

# GUI communication params
IP_ADDRESS = "127.0.0.1"
SEND_PORT = 9100
RECEIVE_PORT = 9101
FORWARD_PORT = 9110
