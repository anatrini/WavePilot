import os

import numpy as np
import pandas as pd

from logger import setup_logger

logging = setup_logger("Data loader")


class DataLoader:
    """Dataloader for loading and preprocessing preset datasets, and extracting preset names."""

    def __init__(self, filepath, mask_columns=None):
        """
        Initialize the DataLoader.

        :param filepath: Path to the dataset CSV file.
        :param mask_columns: List or set of columns to exclude from the dataset (numeric features only).
        """
        if not isinstance(filepath, str):
            raise TypeError("Filepath must be a string representing a valid path to a dataset!")

        self.filepath = filepath
        self.mask_columns = set(mask_columns) if mask_columns else None

        # Internal storage set during `load_presets`
        self._preset_names = None          # list[str], one per row
        self._name_column_used = None      # actual column name used for names (if any)

    def load_presets(self, return_type: str = 'np'):
        """
        Load the dataset from CSV, keep only numeric columns (after optional masking),
        drop all-NaN columns, and return the cleaned matrix.

        Additionally, extract preset names:
        - If a (case-insensitive) 'name' column exists, use it.
        - Otherwise, auto-generate progressive IDs: ID1, ID2, ...

        :param return_type: 'np' to return a numpy array (default), or 'df' to return a pandas DataFrame.
        :return: Cleaned numpy array (float32) or pandas DataFrame (numeric-only).
        """
        _, file_extension = os.path.splitext(self.filepath)

        # Ensure the file is a CSV
        if file_extension.lower() != '.csv':
            raise ValueError(f"Unsupported file type: {file_extension}. Only CSV files are supported.")

        try:
            # Detect separator and read CSV
            separator = self._detect_separator([';', ','])
            df_raw = pd.read_csv(self.filepath, sep=separator)
            logging.info('Dataset loaded with shape %s', df_raw.shape)

            # Extract preset names BEFORE dropping non-numeric columns
            self._preset_names = self._extract_preset_names(df_raw)
            logging.info("Preset names ready (column used: %s)", self._name_column_used or "auto IDs")

            # Apply preprocessing to build the numeric feature matrix
            df = self._preprocess_dataframe(df_raw)
            logging.info("Final dataset shape after preprocessing: %s", df.shape)

            if return_type == 'np':
                return df.to_numpy(dtype=np.float32)
            elif return_type == 'df':
                return df
            else:
                raise ValueError("Return type must be 'np' for numpy or 'df' for pandas DataFrame!")

        except Exception as e:
            # Re-raise with a clean message for the caller
            raise ValueError(f"Error loading file: {e}") from e

    def get_preset_names(self, n_items: int = None):
        """
        Return the list of preset names determined during `load_presets`.
        If `n_items` is provided, ensure the returned list has exactly that length
        (truncate or pad with progressive IDs as needed).

        :param n_items: Optional expected length.
        :return: list[str] of preset names (length equals `n_items` if provided).
        """
        if self._preset_names is None:
            # Not loaded yet; provide a minimal fallback
            if n_items is None:
                return []
            return [f"ID{i+1}" for i in range(n_items)]

        names = list(self._preset_names)
        if n_items is None:
            return names

        # Align length to n_items
        if len(names) >= n_items:
            return names[:n_items]
        else:
            start = len(names) + 1
            names += [f"ID{i}" for i in range(start, n_items + 1)]
            return names

    # ---------------------- internal helpers ----------------------

    def _detect_separator(self, separators):
        """Detect the CSV separator from the first line."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            first_line = file.readline()
            separator = next((sep for sep in separators if sep in first_line), None)
            if not separator:
                raise ValueError(f"No valid separator detected in the file. Checked: {separators}")
            return separator

    def _extract_preset_names(self, df: pd.DataFrame):
        """
        Extract preset names from a 'name' column (case-insensitive).
        Empty/NaN values are replaced with progressive IDs.
        If no 'name' column exists, return progressive IDs for all rows.
        """
        # Find a column named 'name' (case-insensitive)
        name_col = None
        for col in df.columns:
            if isinstance(col, str) and col.lower().strip() == "name":
                name_col = col
                break

        n_rows = len(df)
        ids = [f"ID{i+1}" for i in range(n_rows)]

        if name_col is None:
            self._name_column_used = None
            return ids  # no 'name' column → use IDs

        # Clean values: cast to string, strip whitespace, replace empties with IDi
        series = df[name_col].astype(str)
        names = []
        for i, v in enumerate(series.tolist()):
            s = ("" if v is None else str(v)).strip()
            if s == "" or s.lower() in ("nan", "none"):
                names.append(ids[i])
            else:
                names.append(s)

        self._name_column_used = name_col
        return names

    def _preprocess_dataframe(self, df: pd.DataFrame):
        """Apply all necessary preprocessing steps to the dataset (column-wise)."""
        df = self._drop_id_column(df)
        df = self._remove_non_numeric_columns(df)
        df = self._drop_nan_columns(df)

        if self.mask_columns:
            df = self._mask_columns(df)

        return df

    def _drop_id_column(self, df: pd.DataFrame):
        """Drop the 'ID' column if present (ID values are not used as names)."""
        if 'ID' in df.columns:
            logging.info("Dropping 'ID' column.")
            return df.drop(columns=['ID'])
        return df

    def _remove_non_numeric_columns(self, df: pd.DataFrame):
        """Keep only numeric columns; log which non-numeric columns were removed."""
        numeric_cols = df.select_dtypes(include="number").columns
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        if non_numeric_cols:
            logging.info("Non-numeric columns removed: %s", list(non_numeric_cols))
        return df[numeric_cols]

    def _drop_nan_columns(self, df: pd.DataFrame):
        """Drop columns that are entirely NaN."""
        nan_cols = df.columns[df.isna().all()].tolist()
        if nan_cols:
            logging.info("Columns with all NaN values removed: %s", list(nan_cols))
        return df.dropna(axis=1, how='all')

    def _mask_columns(self, df: pd.DataFrame):
        """Mask specified columns by removing them from the dataset."""
        valid_mask_cols = self.mask_columns.intersection(df.columns)
        if valid_mask_cols:
            logging.info("Masking columns (removing from dataset): %s", list(valid_mask_cols))
            return df.drop(columns=valid_mask_cols)
        return df
