import argparse
import os

import pandas as pd

from logger import setup_logger

# Set up the logger for the DataLoader
logger = setup_logger("Data loader")


class DataLoader:
    def __init__(self, filepath):
        """
        Initialize the DataLoader with the file path.

        :param filepath: Path to the dataset file.
        """
        self.filepath = filepath

    def load_presets(self):
        """
        Load the dataset from a CSV file, remove non-numeric columns,
        columns with all NaN values, and the 'ID' column.

        :return: A cleaned Pandas DataFrame.
        """
        _, file_extension = os.path.splitext(self.filepath)

        try:
            # Ensure the file is a CSV
            if file_extension != ".csv":
                raise ValueError(f"Unsupported file type: {file_extension}. Only CSV files are supported.")

            separator = self._detect_separator([";", ","])
            # Load the CSV with ';' as separator
            df = pd.read_csv(self.filepath, sep=separator)
            logger.info(f"Dataset loaded with shape: {df.shape}")

            # Drop the 'ID' column if present
            if "ID" in df.columns:
                logger.info("Dropping column 'ID' as it is not useful for analysis.")
                df = df.drop(columns=["ID"])

            # Remove non-numeric columns
            df = self._remove_non_numeric_columns(df)

            # Drop columns with all NaN values
            df = self._drop_nan_columns(df)

            logger.info(f"Cleaned dataset shape: {df.shape}")
            return df

        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            raise

    def _detect_separator(self, separators):

        with open(self.filepath, "r") as file:
            first_line = file.readline()
            separator = next((sep for sep in separators if sep in first_line), None)
            if not separator:
                raise ValueError(f"No valid separator detected in the file. Checked: {separators}")
            return separator

    def _remove_non_numeric_columns(self, df):
        """
        Remove non-numeric columns from the dataset and log their names.

        :param df: A Pandas DataFrame.
        :return: A DataFrame with only numeric columns.
        """
        numeric_cols = df.select_dtypes(include="number").columns
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        if non_numeric_cols:
            logger.info(f"Non-numeric columns removed: {non_numeric_cols}")
        return df[numeric_cols]

    def _drop_nan_columns(self, df):
        """
        Drop columns with all NaN values and log their names.

        :param df: A Pandas DataFrame.
        :return: A DataFrame without columns containing all NaN values.
        """
        nan_cols = df.columns[df.isna().all()].tolist()
        if nan_cols:
            logger.info(f"Columns with all NaN values removed: {nan_cols}")
        return df.dropna(axis=1, how="all")


def get_arguments():
    """
    Parse command-line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Load and validate a dataset.")
    parser.add_argument("-f", "--filepath", required=True, type=str, help="Path to the dataset file (CSV).")
    return parser.parse_args()


def main():
    """
    Main function to load and validate the dataset.
    """
    args = get_arguments()

    # Get the filepath from the command-line arguments
    filepath = args.filepath

    try:
        # Initialize DataLoader
        loader = DataLoader(filepath)

        # Load the dataset
        df = loader.load_presets()
        print("Dataset loaded successfully!")
        print(df.head())  # Print the first few rows of the dataset for validation

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
