# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import math
import numpy as np
import optuna
import torch
from torch import nn
from torch.nn import functional as F
from tqdm import tqdm

from utils import to_tensor, compute_hidden_dims, get_device

from constants import (
    MIN_LATENT_DIM, MAX_LATENT_DIM, DATA_MIN, DATA_MAX, DECIMAL_PLACES,
    DEFAULT_KL_BETA, DEFAULT_LEARNING_RATE, DEFAULT_INPUT_NOISE_STD, FINAL_EPOCHS,
    HIDDEN_WIDTH_SCALE_DEFAULT, HIDDEN_DEPTH_DEFAULT, HIDDEN_ROUND_TO_DEFAULT,
    PRUNE_ENABLED_DEFAULT, PRUNE_EVERY_EPOCHS, BEST_IMPROVEMENT_EPS,
    DEFAULT_BATCH_SIZE, GRAD_CLIP_DEFAULT, PER_FEATURE_WEIGHT_MIN,
    RECON_ACCURACY_THRESHOLD
)

# ============================================================
# VAE deterministico per massima ricostruzione (overfitting)
# ============================================================

class DeterministicVAE(nn.Module):
    """
    VAE configured to MAXIMIZE reconstruction on micro datasets.
    Key choices:
      - Deterministic by default: uses z = mu in forward (no sampling noise).
      - Optional KL with a tiny weight (default ~0): does not force latent spread.
      - Decoder ends with Sigmoid: outputs are kept in [0, 1] to match normalized data.
      - No dropout, no weight decay: overfitting is desired.
    """

    def __init__(
        self,
        input_dim: int,
        latent_dim: int = 3,
        hidden_dims: Optional[List[int]] = None,
        kl_beta: float = DEFAULT_KL_BETA,              # ~0: do not penalize "memorization" capacity
        deterministic: bool = True,        # z = mu during both training and evaluation
        input_noise_std: float = DEFAULT_INPUT_NOISE_STD,      # keep 0 by default to avoid hurting reconstruction
    ):
        super().__init__()
        assert MIN_LATENT_DIM <= latent_dim <= MAX_LATENT_DIM, "Latent dimensionality must be between 2 and 4."

        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.kl_beta = float(kl_beta)
        self.deterministic = bool(deterministic)
        self.input_noise_std = float(input_noise_std)

        self.activation = nn.SiLU()

        # Architecture:
        # To maximize reconstruction with very few samples, keep the MLP fairly capacious
        # but not excessively deep. Defaults target 30–120 features with two reasonable hidden layers.
        if hidden_dims is None:
            hidden_dims = compute_hidden_dims(
                input_dim=input_dim,
                latent_dim=latent_dim,
                width_scale=HIDDEN_WIDTH_SCALE_DEFAULT,
                depth=HIDDEN_DEPTH_DEFAULT,
                round_to=HIDDEN_ROUND_TO_DEFAULT
            )

        # Encoder: input -> ... -> (mu, logvar)
        enc_layers = []
        prev = input_dim
        for h in hidden_dims:
            enc_layers += [nn.Linear(prev, h), self.activation]
            prev = h
        self.encoder_backbone = nn.Sequential(*enc_layers)
        self.fc_mu = nn.Linear(prev, latent_dim)
        self.fc_logvar = nn.Linear(prev, latent_dim)

        # Decoder: z -> ... -> x_hat (Sigmoid to enforce [0,1] range)
        dec_layers = []
        prev = latent_dim
        for h in reversed(hidden_dims):
            dec_layers += [nn.Linear(prev, h), self.activation]
            prev = h
        dec_layers += [nn.Linear(prev, input_dim), nn.Sigmoid()]
        self.decoder = nn.Sequential(*dec_layers)

        self._init_weights()

    def _init_weights(self):
        # Kaiming initialization for stability and strong fitting capacity
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_uniform_(m.weight, a=math.sqrt(5))
                if m.bias is not None:
                    fan_in, _ = nn.init._calculate_fan_in_and_fan_out(m.weight)
                    bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0.0
                    nn.init.uniform_(m.bias, -bound, bound)

    def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        h = self.encoder_backbone(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        if self.deterministic:
            return mu
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        return self.decoder(z)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # Optional input noise (disabled by default); keep outputs in [0,1]
        if self.input_noise_std > 0.0 and self.training:
            x = x + torch.randn_like(x) * self.input_noise_std
            x = x.clamp(DATA_MIN, DATA_MAX)
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_hat = self.decode(z)
        return x_hat, mu, logvar

    @staticmethod
    def loss_function(
        x: torch.Tensor,
        x_hat: torch.Tensor,
        mu: torch.Tensor,
        logvar: torch.Tensor,
        kl_beta: float = DEFAULT_KL_BETA,
        per_feature_weights: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Reconstruction term: plain MSE (optionally per-feature weighted in a numerically stable way).
        KL term: optional, weighted by kl_beta (default 0).

        KL equivalences:
          Implemented:  -0.5 * E[ 1 + logvar - mu^2 - exp(logvar) ]
          Common form:   0.5 * E[ mu^2 + exp(logvar) - logvar - 1 ]
          (Algebraically identical)
        """
        if per_feature_weights is None:
            recon = F.mse_loss(x_hat, x, reduction="mean")
        else:
            # Normalize weights so their sum equals feature_dim (keeps scale similar to plain MSE)
            w = per_feature_weights / (per_feature_weights.sum() / per_feature_weights.numel())
            recon = ((x_hat - x) ** 2 * w).mean()

        # KL(q(z|x) || N(0, I)), averaged over the batch (mean reduction)
        kl = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())

        loss = recon + kl_beta * kl
        return loss, recon, kl


# ============================================================
# Wrapper "VectorReducer": API pronta per il tuo flusso
# ============================================================

@dataclass
class TrainConfig:
    epochs: int = FINAL_EPOCHS                            
    lr: float = DEFAULT_LEARNING_RATE                      # Adam without weight decay
    batch_size: int = DEFAULT_BATCH_SIZE                   # 0 => "full batch" (full dataset at once)
    grad_clip: Optional[float] = GRAD_CLIP_DEFAULT         # clipping to prevent spikes
    patience: Optional[int] = None                         # None => no early stopping (overfitting is desirable)
    kl_beta: float = DEFAULT_KL_BETA                       # disabled by default
    deterministic: bool = True                             # z = mu (deterministic)
    input_noise_std: float = DEFAULT_INPUT_NOISE_STD       # disabled by default
    activation: str = "silu"
    hidden_dims: Optional[List[int]] = None
    per_feature_weights: Optional[np.ndarray] = None       # optional: stable wieghting


class VectorReducer:
    """
    Orchestrates:
      - construction and training of the (quasi) deterministic VAE
      - extraction of latent codes μ (to be used later with RBF interpolation)
      - deterministic reconstruction and reconstruction metrics
    """

    def __init__(
        self,
        data: Union[np.ndarray, torch.Tensor],
        latent_dim: int = 3,
        hidden_dims: Optional[List[int]] = None,
        device: Optional[torch.device] = None,
    ):
        assert MIN_LATENT_DIM <= latent_dim <= MAX_LATENT_DIM, "Latent dimensionality must be between 2 and 4."
        self.device = device or get_device()

        # Expect [N, D] tensor in [0,1]; convert to FloatTensor on the target device
        self.X = to_tensor(data, self.device)  # shape: [N, D], normalizzata 0..1
        assert self.X.ndim == 2, "Input data must be [num_samples, num_features]."

        self.num_samples, self.num_features = self.X.shape
        self.latent_dim = latent_dim
        self.hidden_dims = hidden_dims  # may be None: will be computed by policy

        self.model: Optional[DeterministicVAE] = None
        self.best_state: Optional[dict] = None
        self.per_feature_weights_t: Optional[torch.Tensor] = None

    # --------------------------------------------------------

    def _build_model(self, cfg: TrainConfig):
        """Build the DeterministicVAE with either explicit hidden_dims or
           auto-computed ones via compute_hidden_dims policy.
        """
        if cfg.hidden_dims is None:
            hd = compute_hidden_dims(
                input_dim=self.num_features,
                latent_dim=self.latent_dim,
                width_scale=getattr(cfg, "width_scale", HIDDEN_WIDTH_SCALE_DEFAULT),
                depth=getattr(cfg, "depth", HIDDEN_DEPTH_DEFAULT),
                round_to=getattr(cfg, "round_to", HIDDEN_ROUND_TO_DEFAULT)
            )
        else:
            hd = cfg.hidden_dims

        self.model = DeterministicVAE(
            input_dim=self.num_features,
            latent_dim=self.latent_dim,
            hidden_dims=hd,
            kl_beta=cfg.kl_beta,
            deterministic=cfg.deterministic,
            input_noise_std=cfg.input_noise_std,
        ).to(self.device)

        # Optional per-feature weights (stable weighting: clip tiny values, normalization in loss)
        if cfg.per_feature_weights is not None:
            w = np.asarray(cfg.per_feature_weights, dtype=np.float32).reshape(-1)
            assert w.shape[0] == self.num_features, "Per_feature_weights must match num_features!"
            w = np.clip(w, PER_FEATURE_WEIGHT_MIN, None)
            self.per_feature_weights_t = torch.from_numpy(w).to(self.device)
        else:
            self.per_feature_weights_t = None

    # --------------------------------------------------------

    def fit(self,
            cfg: Optional[TrainConfig] = None,
            trial: Optional[optuna.trial.Trial] = None,
            enable_pruning: bool = PRUNE_ENABLED_DEFAULT,
            prune_every: Optional[int] = PRUNE_EVERY_EPOCHS,
            show_progress: bool = False
            ):
        """
        Train the model to overfit (by design) the small dataset.
        Best checkpoint is tracked by reconstruction loss and restored at the end.
        """
        cfg = cfg or TrainConfig()

        if self.model is None:
            self._build_model(cfg)

        model = self.model
        model.train()

        # Optimizer: Adam (no weight decay) to avoid impeding pure fitting
        opt = torch.optim.Adam(model.parameters(), lr=cfg.lr)

        # Full-batch by default (N ≤ 100 typical). Otherwise clamp to N.
        if cfg.batch_size and cfg.batch_size > 0:
            batch_size = min(cfg.batch_size, self.num_samples)
        else:
            batch_size = self.num_samples

        best_recon = float("inf")
        patience_counter = 0

        pbar = tqdm(total=cfg.epochs, disable=not show_progress, desc="Training DVAE")

        for epoch in range(1, cfg.epochs + 1):
            # Simple manual batching: sufficient for tiny datasets
            perm = torch.randperm(self.num_samples, device=self.device)
            epoch_loss = 0.0
            epoch_recon = 0.0
            epoch_kl = 0.0
            nb = 0

            for start in range(0, self.num_samples, batch_size):
                idx = perm[start:start + batch_size]
                batch = self.X[idx]

                x_hat, mu, logvar = model(batch)
                loss, recon, kl = model.loss_function(
                    x=batch, x_hat=x_hat, mu=mu, logvar=logvar,
                    kl_beta=model.kl_beta,
                    per_feature_weights=self.per_feature_weights_t,
                )

                opt.zero_grad(set_to_none=True)
                loss.backward()

                if cfg.grad_clip is not None and cfg.grad_clip > 0:
                    nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)

                opt.step()

                epoch_loss += loss.item()
                epoch_recon += recon.item()
                epoch_kl += kl.item()
                nb += 1

            # Average over mini-batches (usually 1)
            epoch_recon /= max(1, nb)

            if show_progress:
                pbar.set_postfix(recon=f"{epoch_recon:.{DECIMAL_PLACES}f}")
                pbar.update(1)

            # Pruning (not in use)
            if enable_pruning and (trial is not None) and (prune_every is not None) and (prune_every > 0):
                if epoch % prune_every == 0:
                    trial.report(epoch_recon, step=epoch)
                    if trial.should_prune():
                        raise optuna.TrialPruned()

            # Track the best state based on mean reconstruction loss
            if epoch_recon < best_recon - BEST_IMPROVEMENT_EPS:
                best_recon = epoch_recon
                self.best_state = {
                    "model": {k: v.detach().clone() for k, v in model.state_dict().items()},
                    "recon": best_recon,
                    "epoch": epoch,
                }
                patience_counter = 0
            else:
                patience_counter += 1

            # Optional early stopping (disabled by default; overfitting is desired)
            if cfg.patience is not None and patience_counter >= cfg.patience:
                break

        if show_progress:
            pbar.close()

        # Restore best weights to guarantee the best reconstruction achieved
        if self.best_state is not None:
            self.model.load_state_dict(self.best_state["model"])

        self.model.eval()

    # --------------------------------------------------------

    @torch.no_grad()
    def transform(self, data: Optional[Union[np.ndarray, torch.Tensor]] = None) -> np.ndarray:
        """
        Returns deterministic latent codes (μ) for the provided samples.
        These are exactly what you will feed into the RBF interpolator later on.
        """
        assert self.model is not None, "Model is not trained."
        X = self.X if data is None else to_tensor(data, self.device)
        mu, _ = self.model.encode(X)
        return mu.cpu().numpy()

    @torch.no_grad()
    def reconstruct(self, data: Optional[Union[np.ndarray, torch.Tensor]] = None) -> np.ndarray:
        """
        Deterministic recostrunction (decoder(mu)).
        """
        assert self.model is not None, "Model is not trained!"
        X = self.X if data is None else to_tensor(data, self.device)
        mu, _ = self.model.encode(X)
        X_hat = self.model.decode(mu)
        return X_hat.cpu().numpy()

    @torch.no_grad()
    def reconstruction_mse(self, data: Optional[Union[np.ndarray, torch.Tensor]] = None) -> float:
        """
        Mean MSE on [0,1]. With normalized data, this is a reliable measure of reconstruction quality.
        """
        assert self.model is not None, "Model is not trained."
        X = self.X if data is None else to_tensor(data, self.device)
        X_hat = to_tensor(self.reconstruct(X), self.device)
        return F.mse_loss(X_hat, X, reduction="mean").item()

    @torch.no_grad()
    def reconstruction_accuracy(self, threshold: float = RECON_ACCURACY_THRESHOLD, data: Optional[Union[np.ndarray, torch.Tensor]] = None) -> float:
        """
        Percentage of element-wise matches: |x_hat - x| < threshold.
        threshold=0.03 is reasonable for data in [0,1]; adjust as needed.
        """
        assert self.model is not None, "Modello non addestrato."
        X = self.X if data is None else to_tensor(data, self.device)
        X_hat = to_tensor(self.reconstruct(X), self.device)
        diff = (X_hat - X).abs()
        return (diff < threshold).float().mean().item() * 100.0