import json
import pandas as pd


class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_presets(self):

        with open(self.filepath, 'r') as f:
            data = json.load(f)

        # Create a dataframe
        df = pd.DataFrame()
        for key, values in data.items():
            tmp_df = pd.json_normalize(values)
            tmp_df['PRESET_NAME'] = key
            # Add tmp_df to df
            df = pd.concat([df, tmp_df], ignore_index=True)

        df.reset_index(inplace=True)
        df.rename(columns={'index': 'ID'}, inplace=True)

        return df