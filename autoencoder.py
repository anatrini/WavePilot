import numpy as np
import torch

from torch import nn, optim


torch.manual_seed(42)

# class Autoencoder(nn.Module):
#     def __init__(self, input_dim):
#         super(Autoencoder, self).__init__()
#         self.encoder = nn.Sequential(
#             nn.Linear(input_dim, 128),
#             nn.ReLU(True),
#             nn.Linear(128, 64),
#             nn.ReLU(True),
#             nn.Linear(64, 12),
#             nn.ReLU(True),
#             nn.Linear(12, 3))
#         self.decoder = nn.Sequential(
#             nn.Linear(3, 12),
#             nn.ReLU(True),
#             nn.Linear(12, 64),
#             nn.ReLU(True),
#             nn.Linear(64, 128),
#             nn.ReLU(True),
#             nn.Linear(128, input_dim),
#             nn.Tanh())
        
    # def forward(self, x):
    #     x = self.encoder(x)
    #     x = self.decoder(x)
    #     return x
    

# class VectorReducer:
#     def __init__(self, df, learning_rate, weight_decay):
#         self.ids = df['ID'].values
#         self.df = df.drop(columns=['ID', 'PRESET_NAME'])
#         self.model = Autoencoder(self.df.shape[1])
#         self.criterion = nn.MSELoss()
#         self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)

#     def train_autoencoder(self, epochs):
#         self.df = torch.tensor(self.df.values).float()
#         for _ in range(epochs):
#             output = self.model(self.df)
#             loss = self.criterion(output, self.df)
#             self.optimizer.zero_grad()
#             loss.backward()
#             self.optimizer.step()

#     def autoencoder(self):
#         reduced_data = self.model.encoder(self.df).detach().numpy()
#         # Add back ID as the first element of each sublist
#         reduced_data_with_ids = np.column_stack((self.ids, reduced_data))
#         return reduced_data_with_ids
    


class Autoencoder(nn.Module):
    def __init__(self, input_dim, n_layers=1, activation=nn.ReLU()):
        super(Autoencoder, self).__init__()
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
        self.bottleneck = nn.Linear(layer_dims[-1], self.output_dim)

        # Similar for the decoder, but in reverse
        decoder_layers = []
        layer_dims.reverse()  # Reverse the layer dimensions
        layer_dims = [self.output_dim] + layer_dims[:-1]
        for i in range(n_layers):
            decoder_layers.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            decoder_layers.append(activation)
        decoder_layers.append(nn.Linear(layer_dims[-1], input_dim))  # Add a final layer to match the input dimension
        decoder_layers.append(nn.Tanh())
        self.decoder = nn.Sequential(*decoder_layers)

    def forward(self, x):
        encoded = self.encoder(x)
        bottleneck = self.bottleneck(encoded)
        decoded = self.decoder(bottleneck)
        return bottleneck, decoded


class VectorReducer:
    def __init__(self, df, learning_rate, weight_decay, n_layers, activation):
        self.ids = df['ID'].values
        self.df = df.drop(columns=['ID', 'PRESET_NAME'])
        self.model = Autoencoder(self.df.shape[1], n_layers, activation)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    def train_autoencoder(self, epochs):
        self.df = torch.tensor(self.df.values).float()
        for _ in range(epochs):
            bottleneck, output = self.model(self.df)
            loss = self.criterion(output, self.df)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def autoencoder(self):
        with torch.no_grad(): # no need to calculate gradients during evaluation
            bottleneck, _ = self.model(self.df)
        reduced_data = bottleneck.detach().numpy()
        # Add back ID as the first element of each sublist
        reduced_data_with_ids = np.column_stack((self.ids, reduced_data))
        return reduced_data_with_ids