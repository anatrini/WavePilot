# Renderer params
NUM_CHANNELS = 2
SAMPLERATE = 48000
BLOCKSIZE = 1024
AUTOSAVE_INTERVAL = 5
TARGET_dBFS = -3.0
DATASET_FOLDER = "data"
RENDERED_AUDIO_FOLDER = "audio"

# Dataset float numbers resolution
DECIMAL_PLACES = 4

LOG_FOLDER = "./logs"

LATENT_SPACE_SIZE = 3
TORCH_MANUAL_SEED = 12

# Random seeds for reproducibility
OPTUNA_RANDOM_SEED = 56
ENTRY_SELECTION_RANDOM_SEED = 38
TRAIN_TEST_SPLIT_RANDOM_SEED = 42

# VAE parameter ranges, structured by type
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
        "values": [64, 128]
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
    "mse_beta": {
        "type": "float",
        "low": 0.1,
        "high": 1.0,
        "log": False
    }
}

# RBF parameter ranges, structured by type
RBF_PARAM_RANGES = {
    "smoothing": {
        "type": "float",
        "low": 0.5,
        "high": 1.0,
        "log": False
    },
    "kernel": {
        "type": "categorical",
        "values": ["linear", "thin_plate_spline", "cubic", "inverse_quadratic"]
    },
    "epsilon": {
        "type": "float",
        "low": 1.5,
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

RBF_FIXED_EPSILON_KERNELS = ["linear", "thin_plate_spline", "cubic"]

# Number of trials for optimization
N_TRIALS_VAE = 500
N_TRIALS_RBF = 300

# GUI communication params
IP_ADDRESS = "127.0.0.1"
SEND_PORT = 9100
RECEIVE_PORT = 9101
FORWARD_PORT = 9110
