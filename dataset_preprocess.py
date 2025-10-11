import argparse

import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA

from constants import (
    CORRELATION_THRESHOLD,
    DECIMAL_PLACES,
    LOW_VARIANCE_THRESHOLD,
    PCA_VARIANCE_THRESHOLD,
)
from data import DataLoader
from logger import setup_logger

logging = setup_logger("Dataset preprocessor")


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filepath", 
                        dest="filepath", 
                        type=str, 
                        required=True, 
                        help="Input dataset to preprocess.")

    parser.add_argument("-o", "--output", 
                        dest="output", 
                        type=str, 
                        default=None, 
                        help="Output filepath for preprocessed dataset.")

    parser.add_argument("-c", "--columns_to_drop", 
                        dest="columns_to_drop", 
                        nargs="*", 
                        default=[], 
                        help="List of columns to drop.")

    parser.add_argument("-d", "--decimal_places",
                        dest="decimal_places",
                        type=int,
                        default=DECIMAL_PLACES,
                        help="Number of decimal places to round numerical values.")

    return parser.parse_args()


class DatasetPreprocessor:
    def __init__(self, df, output=None, columns_to_drop=None, decimal_places=DECIMAL_PLACES):
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

    def identify_low_variance_features(self, threshold=LOW_VARIANCE_THRESHOLD):
        variances = self.df.var()
        low_variance = variances[variances < threshold].index.tolist()
        logging.info(f"Low-variance features (threshold={threshold}): {low_variance}")
        return low_variance
    
    def find_highly_correlated_features(self, threshold=CORRELATION_THRESHOLD):
        corr_matrix = self.df.corr().abs()
        # Create upper triangular mask (k=1 to exclude diagonal)
        mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        upper = corr_matrix.where(mask)  # Apply mask
        # Find columns with at least one value above threshold
        correlated = [col for col in upper.columns if any(upper[col] > threshold)]
        logging.info(f"Highly correlated features (threshold={threshold}): {correlated}")
        return correlated
    
    def perform_pca_analysis(self, n_components=None, variance_threshold=PCA_VARIANCE_THRESHOLD):
        """
        Perform PCA analysis to identify feature redundancy and intrinsic dataset dimensionality.
    
        :param n_components: Number of principal components to analyze (default: None)
        :param variance_threshold: Cumulative explained variance threshold (default: 0.95)
        """
        # Select numerical columns only
        numeric_data = self.df.select_dtypes(include='number')
    
        # Auto-detect component count if not specified
        if n_components is None:
            n_components = numeric_data.shape[1]
    
        # Initialize and train PCA
        pca = PCA(n_components=n_components)
        pca.fit(numeric_data)
    
        # Calculate cumulative explained variance
        cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    
        # Create variance plot
        fig = px.line(
            x=range(1, n_components + 1),
            y=cumulative_variance,
            title=f"Explained Variance (Threshold: {variance_threshold*100}%)",
            labels={'x': 'Principal Components', 'y': 'Cumulative Variance'}
        )
        fig.add_hline(y=variance_threshold, line_dash="dash", line_color="red")
        fig.show()
    
        # Check threshold achievability
        if np.max(cumulative_variance) < variance_threshold:
            n_components_for_threshold = "Threshold not reached!"
        else:
            n_components_for_threshold = np.argmax(cumulative_variance >= variance_threshold) + 1
            logging.info(f"Components required for {variance_threshold*100}% variance: {n_components_for_threshold}")

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
            self.df.to_csv(self.output, index=False, float_format="%.5f")
        else:
            logging.info("No output file specified. Skipping save.")

    def preprocess(self):
        self.drop_columns()
        self.round_decimals()
        self.drop_duplicates()
        self.check_constant_columns()

        self.identify_low_variance_features()
        self.find_highly_correlated_features()
        self.perform_pca_analysis()

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
    df = loader.load_presets(return_type='df')
    logging.info(df.head())

    preprocessor = DatasetPreprocessor(
        df=df, output=output, columns_to_drop=columns_to_drop, decimal_places=decimal_places
    )
    preprocessor.preprocess()


if __name__ == "__main__":
    main()