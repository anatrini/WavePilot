import argparse
import asyncio
import torch

from data_loader import DataLoader
from torch import nn
from visualizer import Visualizer




def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    parser.add_argument('-e', '--num_epochs',
                      dest='num_epochs',
                      type=int,
                      default=100)
    
    parser.add_argument('-l', '--learning_rate',
                      dest='learning_rate',
                      type=float,
                      default=1e-3)
    
    # L1/L2 regularization (search space [1e-5, 1e-3])
    parser.add_argument('-w', '--weight_decay',
                      dest='weight_decay',
                      type=float,
                      default=1e-3)
    
    return parser.parse_args()



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
    

class DimensionReducer:
    def __init__(self, df, learning_rate, weight_decay):
        self.df = df.drop(columns=['PRESET_NAME'])
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
        return self.model.encoder(self.df).detach().numpy()



def main():
    IP_ADDRESS = '127.0.0.1'
    PORT = 5105

    args = get_arguments()
    filepath = args.filepath
    num_epochs = args.num_epochs
    learning_rate = args.learning_rate
    weight_decay = args.weight_decay

    loader = DataLoader(filepath)
    df = loader.load_presets()

    reducer = DimensionReducer(df, learning_rate, weight_decay)
    reducer.train_autoencoder(num_epochs)
    reduced_data = reducer.autoencoder()
    visualizer = Visualizer(reduced_data)
    asyncio.run(visualizer.run(IP_ADDRESS, PORT))


if __name__ == '__main__':
    main()