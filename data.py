import os

import numpy as np
import pandas as pd

from logger import setup_logger

logging = setup_logger("Data loader")


class DataLoader:
    """Dataloader for loading and preprocessing preset datasets."""

    def __init__(self, filepath, mask_columns=None):
        """
        Initialize the DataLoader.

        :param filepath: Path to the dataset CSV file.
        :param mask_columns: List or set of columns to exclude from the dataset.
        """
        if not isinstance(filepath, str):
            raise TypeError("Filepath must be a string representing a valid path to a dataset!")
        
        self.filepath = filepath
        self.mask_columns = set(mask_columns) if mask_columns else None

    def load_presets(self):
        """
        Load the dataset from a CSV file, remove non-numeric columns,
        columns with all NaN values, and the 'ID' column;
        Convert Pandas' Dataframe to array.

        :return: a cleaned numpy.array.
        """
        _, file_extension = os.path.splitext(self.filepath)

        # Ensure the file is a CSV and set the proper separator
        if file_extension != '.csv':
            raise ValueError("Unsupported file type: %s. Only CSV files are supported.", file_extension)

        try:
            separator = self._detect_separator([';', ','])
            df = pd.read_csv(self.filepath, sep=separator)
            logging.info('Dataset loaded with shape %s', df.shape)

            df = self._preprocess_dataframe(df)

            logging.info("Final dataset shape after preprocessing: %s", df.shape)
            return df.to_numpy(dtype=np.float32)

        except Exception as e:
            raise ValueError("Error loading file: %s", e)

    def _detect_separator(self, separators):

        with open(self.filepath, 'r', encoding='utf-8') as file:
            first_line = file.readline()
            separator = next((sep for sep in separators if sep in first_line), None)
            if not separator:
                raise ValueError("No valid separator detected in the file. Checked: %s", separators)
            return separator
        
    def _preprocess_dataframe(self, df):
        """Apply all necessary preprocessing steps to the dataset."""
        df = self._drop_id_column(df)
        df = self._remove_non_numeric_columns(df)
        df = self._drop_nan_columns(df)

        if self.mask_columns:
            df = self._mask_columns(df)

        return df
    

    def _drop_id_column(self, df):
        """Drop the 'ID' column if present."""
        if 'ID' in df.columns:
            logging.info("Dropping 'ID' column.")
            return df.drop(columns=['ID'])
        return df

    def _remove_non_numeric_columns(self, df):
        numeric_cols = df.select_dtypes(include="number").columns
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        if non_numeric_cols:
            logging.info("Non-numeric columns removed: %s", list(non_numeric_cols))
        return df[numeric_cols]

    def _drop_nan_columns(self, df):
        nan_cols = df.columns[df.isna().all()].tolist()
        if nan_cols:
            logging.info("Columns with all NaN values removed: %s", list(nan_cols))
        return df.dropna(axis=1, how='all')
    

    def _mask_columns(self, df):
        """Mask specified columns by removing them from the dataset."""
        valid_mask_cols = self.mask_columns.intersection(df.columns)
        if valid_mask_cols:
            logging.info("Masking columns (removing from dataset): %s", list(valid_mask_cols))
            return df.drop(columns=valid_mask_cols)
        return df
