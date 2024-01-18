import numpy as np
import torch

from torch import nn


torch.manual_seed(42)

class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True),
            nn.Linear(64, 12),
            nn.ReLU(True),
            nn.Linear(12, 3))
        self.decoder = nn.Sequential(
            nn.Linear(3, 12),
            nn.ReLU(True),
            nn.Linear(12, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True),
            nn.Linear(128, input_dim),
            nn.Tanh())
        
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
    

class VectorsReducer:
    def __init__(self, df, learning_rate, weight_decay):
        self.ids = df['ID'].values
        self.df = df.drop(columns=['ID', 'PRESET_NAME'])
        self.model = Autoencoder(self.df.shape[1])
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    def train_autoencoder(self, epochs):
        self.df = torch.tensor(self.df.values).float()
        for _ in range(epochs):
            output = self.model(self.df)
            loss = self.criterion(output, self.df)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def autoencoder(self):
        reduced_data = self.model.encoder(self.df).detach().numpy()
        # Add back ID as the first element of each sublist
        reduced_data_with_ids = np.column_stack((self.ids, reduced_data))
        return reduced_data_with_ids