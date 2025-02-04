import torch

from torch import nn, optim
from utils import get_device


torch.manual_seed(42)

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

        self.output_dim = 3 # make default
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
        std = torch.exp(0.5 * logvar) # verificare
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
    def __init__(self, df, learning_rate, weight_decay, n_layers, layer_dim, activation, kl_beta, mse_beta, pretrained_model=None):

        self.device = get_device()
        self.df: torch.Tensor = torch.tensor(df).float()

        if pretrained_model is None:
            self.model = VAE(self.df.shape[1], n_layers, layer_dim, activation).to(self.device)
        else:
            self.model = pretrained_model.to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        self.kl_beta = kl_beta
        self.mse_beta = mse_beta

    def kl_divergence(self, mu, logvar):
        return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    
    def compute_loss(self, data, compute_gradients=False):
        # Move data on the device
        data = data.to(self.device)

        mu, logvar, output = self.model(data)
        recon_loss = self.criterion(output, data)
        kl_loss = self.kl_divergence(mu, logvar)
        mse_loss = (output - data).pow(2).mean()

        # Weighted sum of losses
        loss = recon_loss + (kl_loss * self.kl_beta) + (mse_loss * self.mse_beta)

        if compute_gradients:
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        return loss.item()

    def train_vae(self, epochs):
        for _ in range(epochs):
            self.compute_loss(self.df, compute_gradients=True)

    def vae(self):
        device = next(self.model.parameters()).device
        print(f"Model is on device: {device}")
        print(f"Input data is on device: {self.df.device}")
        with torch.no_grad(): # no need to calculate gradients during evaluation
            mu, _, decoded = self.model(self.df.to(device))
        reduced_data = mu.detach().cpu().numpy()
        reconstructed_data = decoded.detach().cpu().numpy()
        return reduced_data, reconstructed_data
    
    def move_to_cpu(self):
        #Move the model to CPU. This method centralizes the logic for device handling
        self.model = self.model.to('cpu')
        self.df = self.df.to('cpu')