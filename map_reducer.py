import argparse

from data_loader import DataLoader
from sklearn.manifold import Isomap
from umap import UMAP
from visualizer import Visualizer




def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filepath',
                      dest='filepath',
                      type=str,
                      default=None)
    
    parser.add_argument('-r', '--reduction',
                      dest='reduction',
                      type=str,
                      default='umap')
    
    return parser.parse_args()



class DimensionReducer:
    def __init__(self, df):
        self.df = df.drop(columns=['PRESET_NAME']) # exclude ID column
        self.methods = {
            'umap': self.umap,
            'isomap': self.isomap
        }

    def umap(self):
        reducer = UMAP(n_components=3, random_state=42)
        return reducer.fit_transform(self.df.values)
    
    def isomap(self):
        iso = Isomap(n_components=3)
        return iso.fit_transform(self.df.values)
    
    def reduce(self, method):
        if method in self.methods:
            return self.methods[method]()
        else:
            raise ValueError(f'Unknown reduction method: {method}')
    

def main():
    args = get_arguments()
    filepath = args.filepath
    reduction = args.reduction

    loader = DataLoader(filepath)
    df = loader.load_presets()

    reducer = DimensionReducer(df)
    try:
        reduced_data = reducer.reduce(reduction)
    except ValueError as e:
        print(e)
        return

    visualizer = Visualizer(reduced_data, df)
    visualizer.visualize()



if __name__ == '__main__':
    main()