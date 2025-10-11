# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WavePilot is a framework for exploring Digital Multimedia Instrument (DMmI) parameter spaces using Variational Autoencoders (VAE) and Radial Basis Function (RBF) interpolation. It creates a 3D navigable representation of audio plugin presets, enabling intuitive parameter control through cursor movement in a virtual space.

**Core workflow**: VAE reduces high-dimensional plugin parameters (30-120 params) to 2-4D latent space → RBF interpolation maps cursor positions to parameter values → Real-time OSC communication with REAPER/plugins.

## Environment Setup

**Create and activate conda environment:**
```bash
conda env create -f environment.yml
conda activate wp
```

**Required external dependencies** (not in environment.yml):
- REAPER DAW (hosts plugins and handles preset rendering)
- Blackhole (audio routing): `brew install blackhole`
- Max (with odot library) for controller patch

**System compatibility**: macOS only (tested).

## Common Commands

### Dataset Generation (REAPER must be running with plugin loaded)

**Export factory/user presets to CSV:**
```bash
python plugin_renderer.py -m preset -d <blackhole_device_id>
```

**Generate random presets with silence filtering:**
```bash
python plugin_renderer.py -m random -d <blackhole_device_id> -t <silence_threshold>
```

### Hyperparameter Optimization

**Run unified optimization (VAE + RBF):**
```bash
python main.py optimize -f <dataset.csv>
```

**With dataset subsampling and parameter masking:**
```bash
python main.py optimize -f <dataset.csv> -n <num_entries> -m <param1> <param2>
```

### Training and Visualization

**Train from optimization log:**
```bash
python main.py train -f <dataset.csv> -o <optimizer_log.log>
```

**Train from pretrained model:**
```bash
python main.py train -f <dataset.csv> -p <model.pt>
```

**Save trained model:**
```bash
python main.py train -f <dataset.csv> -o <log.log> -s <output_model.pt>
```

**Access web interface**: After training starts, navigate to `http://127.0.0.1:5000`

### Parameter Control (requires REAPER running with plugin)

**In separate terminal after training is running:**
```bash
python plugin_setter.py
```

**Controller**: Open `wavepilot_controller.maxpat` in Max for cursor control via trajectories or smart device (ZIG SIM app).

## Architecture

### Data Flow Pipeline

1. **Dataset preparation** (`plugin_renderer.py`): REAPER renders presets → audio + CSV with normalized [0,1] parameter values
2. **Optimization** (`optimize.py`): Optuna search for VAE + RBF hyperparameters (parallel workers, deterministic seeds)
3. **Training** (`train.py`): VAE training → latent encoding → RBF fitting with optional z-score normalization
4. **Runtime** (`visualizer.py` + `socket_handlers.py`): OSC ingress → interpolation → Socket.IO updates → OSC egress to REAPER

### Key Modules

**`model.py`** - Deterministic VAE architecture:
- `DeterministicVAE`: Maximizes reconstruction on micro datasets (10-100 presets)
- `VectorReducer`: Training orchestrator with overfitting-by-design strategy
- Uses μ (mean) directly without sampling noise during both training and inference
- KL weight β ≈ 0 (no latent spread penalty)

**`interpolator.py`** - RBF interpolation wrapper:
- Maps UI cursor coords [-1,1]ᵏ to latent space coordinates
- Handles per-dimension denormalization based on latent bounds
- NN-blend safety feature: smooth fallback to nearest preset at sparse regions
- `send_data()`: per-parameter OSC message dispatch using address list

**`optimize.py`** - Two-stage hyperparameter search:
- Stage 1: VAE params (learning rate, KL beta, architecture) via parallel ProcessPool workers
- Stage 2: RBF params (kernel, smoothing, epsilon_scale, degree) with Mahalanobis validation metric
- Epsilon computed as `epsilon_scale × median_pairwise_distance` in latent space
- Results logged to `logs/` folder with space fingerprints

**`train.py`** - Flask + Socket.IO server:
- Async entry point: loads/trains VAE → builds RBF → starts web server (thread) + OSC server (async)
- Exposes `/` (UI) and `/data` (latent points) routes
- Socket.IO handlers: `cursor_move` (browser→server), `addr_list` (address registration)

**`visualizer.py`** - OSC → Socket.IO bridge:
- Listens on `FORWARD_PORT` (9901) for `/cursor [x y z]` from Max controller
- Computes interpolated values for UI feedback only
- Emits `cursor_update` to browser (does NOT send to REAPER here)

**`socket_handlers.py`** - Browser cursor handling:
- Receives cursor from browser UI
- Anti-flood throttling (30 Hz max, epsilon dedupe)
- Sends parameter values to REAPER via `interpolator.send_data()` on `SEND_PORT` (9902)

**`constants.py`** - Centralized configuration:
- OSC ports: `RECEIVE_PORT` (9900), `FORWARD_PORT` (9901), `SEND_PORT` (9902)
- Search space definitions: `VAE_PARAM_RANGES`, `RBF_PARAM_RANGES`
- Training defaults: `FINAL_EPOCHS=4000`, `SEARCH_EPOCHS=600`
- NN-blend UX tuning: `NN_BLEND_SCALE=1.5`, `NN_BLEND_POWER=2.0`

### OSC Communication Architecture

Three-port system for message routing:

```
Controller (Max) --[/cursor]--> FORWARD_PORT (9901) --> Visualizer
                                                           ↓
                                                    Socket.IO (browser UI)
                                                           ↓
Browser UI --[cursor_move]--> Socket.IO server --> Interpolator
                                                           ↓
                                              SEND_PORT (9902) --> REAPER (ReaLearn)
```

**Important**: Parameter egress to REAPER happens ONLY in `socket_handlers.cursor_move()` with anti-flood protection.

### State Management

- **Latent space normalization**: Optional z-score applied ONCE after VAE encoding, before RBF fitting
- **Scaler persistence**: Saved in model checkpoints (`.pt`) via `serialization.py`
- **Coordinate mapping**: Cursor [-1,1] → latent bounds min/max per dimension → RBF query point
- **Global seed**: `GLOBAL_SEED=56` + trial number for reproducible parallel trials

## Dataset and Model Files

- **Datasets**: `data/*.csv` (normalized [0,1] parameter values + preset names)
- **Rendered audio**: `audio/<plugin_name>/*.wav`
- **Models**: `checkpoints/*.pt` (contains VAE state_dict, hyperparams, latent scaler, RBF params)
- **Optimization logs**: `logs/*.log` (timestamped, contains best hyperparameters)
- **OSC address maps**: `addresses/*.json` (parameter name → OSC path mappings)

## Testing

Run pytest on test files (if present):
```bash
pytest
```

## Development Notes

- **Overfitting is intentional**: Small datasets (10-100 presets) require memorization, not generalization
- **Deterministic VAE**: No sampling noise (z = μ) ensures exact reconstruction at anchor points
- **RBF epsilon**: Relative scaling via `epsilon_scale` × median distance improves robustness across latent geometries
- **NN-blend**: Safety net for cursor positions near latent space boundaries (reduces interpolation spikes)
- **Parallel optimization**: VAE trials run on CPU workers (ProcessPool), RBF trials sequential (n_jobs=1)
- **Port conflicts**: Ensure ports 5000, 9900-9902 are available before running

## REAPER Project Files

- `reaper/WP-OBXd-Tester.RPP`: Example project for OBXd plugin
- `reaper/WP-Adaptiverb-Tester.RPP`: Example project for Adaptiverb plugin

Load these in REAPER to test preset rendering and parameter control workflows.
