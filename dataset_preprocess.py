import argparse
from decimal import Decimal

import numpy as np
import pandas as pd
import plotly.express as px

from data import DataLoader
from logger import setup_logger

logging = setup_logger("Dataset preprocessor")


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--filepath", dest="filepath", type=str, required=True, help="Input dataset to preprocess."
    )

    parser.add_argument(
        "-o", "--output", dest="output", type=str, default="None", help="Output filepath for preprocessed dataset."
    )

    parser.add_argument(
        "-c", "--columns_to_drop", dest="columns_to_drop", nargs="*", default=[], help="List of columns to drop."
    )

    parser.add_argument(
        "-d",
        "--decimal_places",
        dest="decimal_places",
        type=int,
        default=4,
        help="Number of decimal places to round numerical values.",
    )

    return parser.parse_args()


class DatasetPreprocessor:
    def __init__(self, df, output=None, columns_to_drop=None, decimal_places=3):
        self.df = df
        self.output = output
        self.columns_to_drop = columns_to_drop
        self.decimal_places = decimal_places

    def drop_columns(self):
        if self.columns_to_drop:
            logging.info(f"Dropping columns: {self.columns_to_drop}")
            self.df = self.df.drop(columns=self.columns_to_drop, errors="ignore")
        else:
            logging.info("No columns specified to drop. Skipping this step.")

    def round_decimals(self):
        if self.decimal_places:
            logging.info(f"Rounding decimals to {self.decimal_places} places...")
            # Detect if normalization is needed
            self.df = np.round(self.df, decimals=self.decimal_places)

        else:
            logging.info("No rounding specified. Skipping this step.")

    def drop_duplicates(self):
        logging.info("Dropping duplicate rows...")
        self.df = self.df.drop_duplicates()

    def check_constant_columns(self):
        constant_columns = [col for col in self.df.columns if self.df[col].nunique() <= 1]
        if constant_columns:
            logging.info(f"Constant columns found: {constant_columns}")
        else:
            logging.info("No constant columns found.")

    def generate_correlation_heatmap(self):
        numeric_columns = self.df.select_dtypes(include="number").columns
        if len(numeric_columns) == 0:
            logging.info("No numeric columns found for correlation heatmap.")
            return

        correlation_matrix = self.df[numeric_columns].corr()
        fig = px.imshow(
            correlation_matrix,
            title="Correlation Heatmap",
            color_continuous_scale="rainbow",
            labels={"color": "Correlation"},
            x=numeric_columns,
            y=numeric_columns,
        )
        fig.show()

    def generate_boxplot(self):
        df_long = self.df.melt(var_name="Column", value_name="Value")
        fig = px.box(
            df_long,
            x="Column",
            y="Value",
            points="all",
            color="Column",
            title="Boxplot of Numeric Columns",
            labels={"Value": "Value", "Column": "Feature"},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )

        fig.update_layout(
            legend_title_text="Columns",
            xaxis_title="Feature",
            yaxis_title="Variance",
            title=dict(text="Boxplot of Numeric Columns", x=0.5),
        )
        fig.show()

    def generate_variance_plot(self):
        variances = self.df.var()

        fig = px.bar(
            x=variances.index,
            y=variances.values,
            title="Variance of Numeric Columns",
            labels={"x": "Feature", "y": "Variance"},
            color=variances.values,
            color_continuous_scale="Viridis",
        )

        fig.update_layout(
            xaxis_title="Feature", yaxis_title="Variance", title=dict(text="Variance of Numeric Columns", x=0.5)
        )
        fig.show()

    def generate_histogram(self):
        numeric_columns = self.df.select_dtypes(include="number").columns
        if len(numeric_columns) == 0:
            logging.info("No numeric columns found for correlation heatmap.")
            return

        df_long = self.df[numeric_columns].melt(var_name="Column", value_name="Value")

        fig = px.histogram(
            df_long,
            x="Value",
            color="Column",
            barmode="overlay",
            nbins=30,
            title="Aggregated Histogram of Numeric Columns",
            labels={"Value": "Value", "Column": "Column"},
        )
        fig.update_layout(
            legend_title_text="Columns",
            xaxis_title="Value",
            yaxis_title="Frequency",
            title=dict(text="Aggregated Histogram of Numeric Columns", x=0.5),
        )
        fig.update_traces(opacity=0.6)
        fig.show()

    def save_dataset(self):
        if self.output:
            logging.info("Saving preprocessed dataset to {self.output}...")
            self.df.to_csv(self.output, index=False, float_format="%.4f")
        else:
            logging.info("No output file specified. Skipping save.")

    def preprocess(self):
        self.drop_columns()
        self.round_decimals()
        self.drop_duplicates()
        self.check_constant_columns()
        self.generate_correlation_heatmap()
        self.generate_boxplot()
        self.generate_variance_plot()
        self.save_dataset()


def main():
    args = get_arguments()
    filepath = args.filepath
    output = args.output
    columns_to_drop = args.columns_to_drop
    decimal_places = args.decimal_places

    loader = DataLoader(filepath)
    df = loader.load_presets()
    logging.info(df.head())

    preprocessor = DatasetPreprocessor(
        df=df, output=output, columns_to_drop=columns_to_drop, decimal_places=decimal_places
    )
    preprocessor.preprocess()


if __name__ == "__main__":
    main()
