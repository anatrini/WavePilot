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
DECIMAL_PLACES = 5
LOW_VARIANCE_THRESHOLD = 0.01
CORRELATION_THRESHOLD = 0.95
PCA_VARIANCE_THRESHOLD = 0.95

LOG_FOLDER = "./logs"

#LATENT_SPACE_SIZE = 3 # overwritten by latent_dim
#TORCH_MANUAL_SEED = 12

# Random seeds for reproducibility
GLOBAL_SEED = 56

# VAE parameter ranges, structured by type
LOSS_EPSILON = 1e-08 # to prevent numerical instability

VAE_PARAM_RANGES = {
    "num_epochs": {
        "type": "categorical",
        "values": [50, 100]
    },
    "learning_rate": {
        "type": "float",
        "low": 1e-5,
        "high": 1e-2,
        "log": True
    },
    "weight_decay": {
        "type": "float",
        "low": 1e-6,
        "high": 1e-4,
        "log": True
    },
    "n_layers": {
        "type": "int",
        "low": 1,
        "high": 2
    },
    "layer_dim": {
        "type": "categorical",
        "values": [16, 32, 64]
    },
    "activation_function": {
        "type": "categorical",
        "values": ["ELU", "GELU", "LeakyReLU"]
    },
    "kl_beta": {
        "type": "float",
        "low": 0.01,
        "high": 0.5,
        "log": False
    },
    "recon_alpha": {
        "type": "float",
        "low": 1.0,
        "high": 5.0,
        "log": False
    },
    "dropout_rate": {
        "type": "float",
        "low": 0.0,
        "high": 0.4,
        "log": False
    },
    "latent_dim": {
        "type": "categorical",
        "values": [2, 3, 4]
    },
    "kl_threshold": {
        "type": "float",
        "low": 0.01,
        "high": 0.1,
        "log": True
    },
    "annealing_epochs": {
        "type": "int",
        "low": 10,
        "high": 30
    }
}

# RBF parameter ranges, structured by type
RBF_PARAM_RANGES = {
    "smoothing": {
        "type": "float",
        "low": 0.5,
        "high": 2.0,
        "log": False
    },
    "kernel": {
        "type": "categorical",
        #"values": ["linear", "thin_plate_spline", "cubic", "inverse_quadratic", "gaussian"]
        "values": ["thin_plate_spline", "cubic", "inverse_quadratic", "linear"]
    },
    "epsilon": {
        "type": "float",
        "low": 0.5,
        "high": 2.0,
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

RBF_FIXED_EPSILON_KERNELS = ["linear", "thin_plate_spline", "cubic"]

# Number of trials for optimization
N_TRIALS_VAE = 500
N_TRIALS_RBF = 300

# GUI communication params
IP_ADDRESS = "127.0.0.1"
SEND_PORT = 9100
RECEIVE_PORT = 9101
FORWARD_PORT = 9110
