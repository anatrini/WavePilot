import numpy as np
import torch
from torch import nn, optim

from constants import LATENT_SPACE_SIZE, TORCH_MANUAL_SEED
from utils import get_device

torch.manual_seed(TORCH_MANUAL_SEED)


class VAE(nn.Module):
    def __init__(self, input_dim, n_layers, layer_dim, activation):
        super(VAE, self).__init__()
        encoder_layers = []
        layer_dims = [input_dim]
        for i in range(n_layers):
            encoder_layers.append(nn.Linear(layer_dims[-1], layer_dim))
            encoder_layers.append(activation)
            layer_dims.append(layer_dim)  # Save the layer dimension
            if i < n_layers - 1:  # Decrease the size of the next layer only if it's not the last layer
                layer_dim = layer_dim // 2
        self.encoder = nn.Sequential(*encoder_layers)

        self.output_dim = LATENT_SPACE_SIZE
        self.fc_mu = nn.Linear(layer_dims[-1], self.output_dim)
        self.fc_var = nn.Linear(layer_dims[-1], self.output_dim)

        # Similar for the decoder, but in reverse
        decoder_layers = []
        layer_dims.reverse()  # Reverse the layer dimensions
        layer_dims = [self.output_dim] + layer_dims[:-1]
        for i in range(n_layers):
            decoder_layers.append(nn.Linear(layer_dims[i], layer_dims[i + 1]))
            decoder_layers.append(activation)
        decoder_layers.append(nn.Linear(layer_dims[-1], input_dim))  # Add a final layer to match the input dimension
        decoder_layers.append(nn.Sigmoid())  
        self.decoder = nn.Sequential(*decoder_layers)

    def reparametrize(self, mu, logvar):
        std = torch.exp(0.5 * logvar) 
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        encoded = self.encoder(x)
        mu = self.fc_mu(encoded)
        logvar = self.fc_var(encoded)
        z = self.reparametrize(mu, logvar)
        decoded = self.decoder(z)
        return mu, logvar, decoded


class VectorReducer:
    def __init__(
        self,
        df,
        learning_rate=None,
        weight_decay=None,
        n_layers=None,
        layer_dim=None,
        activation=None,
        kl_beta=None,
        mse_beta=None,
        pretrained_model=None
    ):
        self.device = get_device()

        self.df = torch.tensor(df).float().to(self.device)

        if pretrained_model is not None:
            self.model = pretrained_model.to(self.device)
            self.model.eval()

            self.optimizer = None
            self.kl_beta = None
            self.mse_beta = None

        else:
            # Training from scratch
            self.model = VAE(self.df.shape[1], n_layers, layer_dim, activation).to(self.device)

            self.kl_beta = kl_beta
            self.mse_beta = mse_beta
            self.criterion = nn.MSELoss()
            self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    def kl_divergence(self, mu, logvar):
        return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    def compute_loss(self, data, compute_gradients=False):
        if isinstance(data, np.ndarray):
            data = torch.tensor(data).float()
        data = data.to(self.device)

        mu, logvar, output = self.model(data)
        recon_loss = self.criterion(output, data)
        kl_loss = self.kl_divergence(mu, logvar)
        mse_loss = (output - data).pow(2).mean()

        loss = recon_loss + (kl_loss * self.kl_beta) + (mse_loss * self.mse_beta)

        if compute_gradients:
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        return loss.item()

    def train_vae(self, epochs):
        if self.df is None:
            raise ValueError("Training data not available (df is None). Cannot train model.")
        for _ in range(epochs):
            self.compute_loss(self.df, compute_gradients=True)

    def vae(self):
        if self.df is None:
            raise ValueError("Dataset not available (df is None). Cannot compute latent representation.")
        with torch.no_grad():
            mu, _, decoded = self.model(self.df.to(self.device))
        return mu.cpu().numpy(), decoded.cpu().numpy()

    def move_to_cpu(self):
        self.model = self.model.to("cpu")
        if self.df is not None:
            self.df = self.df.to("cpu")