import numpy as np
import torch

from torch import nn, optim
from torchviz import make_dot


torch.manual_seed(42)

class VAE(nn.Module):
    def __init__(self, input_dim, n_layers=1, activation=nn.ReLU()):
        super(VAE, self).__init__()
        encoder_layers = []
        layer_dims = [input_dim]
        layer_dim = 128
        for i in range(n_layers):
            encoder_layers.append(nn.Linear(layer_dims[-1], layer_dim))
            encoder_layers.append(activation)
            layer_dims.append(layer_dim)  # Save the layer dimension
            if i < n_layers - 1:  # Decrease the size of the next layer only if it's not the last layer
                layer_dim = layer_dim // 2
        self.encoder = nn.Sequential(*encoder_layers)

        self.output_dim = 3
        self.fc_mu = nn.Linear(layer_dims[-1], self.output_dim)
        self.fc_var = nn.Linear(layer_dims[-1], self.output_dim)

        # Similar for the decoder, but in reverse
        decoder_layers = []
        layer_dims.reverse()  # Reverse the layer dimensions
        layer_dims = [self.output_dim] + layer_dims[:-1]
        for i in range(n_layers):
            decoder_layers.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            decoder_layers.append(activation)
        decoder_layers.append(nn.Linear(layer_dims[-1], input_dim))  # Add a final layer to match the input dimension
        decoder_layers.append(nn.Sigmoid()) # nn.Sigmoid()
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
    def __init__(self, df, learning_rate, weight_decay, n_layers, activation, beta, pretrained_model=None):
        self.ids = df['ID'].values
        self.df = df.drop(columns=['ID', 'name', 'file'])
        if pretrained_model is None:
            self.model = VAE(self.df.shape[1], n_layers, activation)
        else:
            self.model = pretrained_model
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        self.beta = beta

    def kl_divergence(self, mu, logvar):
        return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    def train_vae(self, epochs):
        self.df = torch.tensor(self.df.values).float()
        for _ in range(epochs):
            mu, logvar, output = self.model(self.df)
            recon_loss = self.criterion(output, self.df)
            kl_loss = self.kl_divergence(mu, logvar)
            loss = recon_loss + kl_loss * self.beta
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def vae(self):
        with torch.no_grad(): # no need to calculate gradients during evaluation
            mu, _, decoded = self.model(self.df)
        reduced_data = mu.detach().numpy()
        reconstructed_data = decoded.detach().numpy()
        # Add back ID as the first element of each sublist
        reduced_data_with_ids = np.column_stack((self.ids, reduced_data))
        return reduced_data_with_ids, reconstructed_data
    
    def visualize_model(self):
        x = torch.randn(1, self.df.shape[1])
        mu, _, _ = self.model(x)
        return make_dot(mu, params=dict(self.model.named_parameters()))