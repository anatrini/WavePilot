import json
import os
import pandas as pd

from logger import setup_logger

logging = setup_logger('Data loader')

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_presets(self):

        _, file_extension = os.path.splitext(self.filepath)

        try:
            if file_extension == '.json':
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
            elif file_extension == '.csv':
                df = pd.read_csv(self.filepath)
            else:
                raise ValueError(f'Unsupported file type: {file_extension}')
            
            return df
        
        except Exception as e:
            logging.error(str(e))