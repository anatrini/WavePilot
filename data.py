import os

import numpy as np
import pandas as pd

from logger import setup_logger

logging = setup_logger("Data loader")


class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_presets(self):
        """
        Load the dataset from a CSV file, remove non-numeric columns,
        columns with all NaN values, and the 'ID' column;
        Convert Pandas' Dataframe to array.

        :return: a cleaned numpy.array.
        """
        _, file_extension = os.path.splitext(self.filepath)

        try:
            # Ensure the file is a CSV and set the proper separator
            if file_extension != ".csv":
                raise ValueError(f"Unsupported file type: {file_extension}. Only CSV files are supported.")

            separator = self._detect_separator([";", ","])
            df = pd.read_csv(self.filepath, sep=separator)
            logging.info(f"Dataset loaded with shape: {df.shape}")

            # Drop the 'ID' column if present
            if "ID" in df.columns:
                logging.info("Dropping column 'ID' as it is not useful for analysis.")
                df = df.drop(columns=["ID"])

            # Remove non-numeric columns and NaN values
            df = self._remove_non_numeric_columns(df)
            df = self._drop_nan_columns(df)

            logging.info(f"Cleaned dataset shape: {df.shape}")
            return df.to_numpy(dtype=np.float32)

        except Exception as e:
            logging.error(f"Error loading file: {str(e)}")
            raise

    def _detect_separator(self, separators):

        with open(self.filepath, "r") as file:
            first_line = file.readline()
            separator = next((sep for sep in separators if sep in first_line), None)
            if not separator:
                raise ValueError(f"No valid separator detected in the file. Checked: {separators}")
            return separator

    def _remove_non_numeric_columns(self, df):
        numeric_cols = df.select_dtypes(include="number").columns
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        if non_numeric_cols:
            logging.info(f"Non-numeric columns removed: {non_numeric_cols}")
        return df[numeric_cols]

    def _drop_nan_columns(self, df):
        nan_cols = df.columns[df.isna().all()].tolist()
        if nan_cols:
            logging.info(f"Columns with all NaN values removed: {nan_cols}")
        return df.dropna(axis=1, how="all")
