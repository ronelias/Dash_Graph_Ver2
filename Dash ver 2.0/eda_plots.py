import os
from datetime import datetime
from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

def save_eda_plots(df: pd.DataFrame, output_dir: str) -> Dict[str, str]:
    """
    Generate and save EDA plots (correlation heatmap, missing value heatmap),
    returning a dictionary with their file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    paths = {}

    numeric = df.select_dtypes(include="number")

    if numeric.shape[1] >= 2:
        try:
            corr = numeric.corr()
            plt.figure(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
            plt.title("Correlation Matrix")
            plt.tight_layout()
            corr_path = os.path.join(output_dir, f"correlation_heatmap_{timestamp}.png")
            plt.savefig(corr_path)
            plt.close()
            paths["correlation"] = corr_path
        except Exception as e:
            print(f"❌ Failed to generate correlation heatmap: {e}")

    if df.isnull().values.any():
        try:
            msno.heatmap(df, figsize=(10, 6), fontsize=12)
            plt.title("Missing Values Heatmap")
            plt.tight_layout()
            miss_path = os.path.join(output_dir, f"missing_heatmap_{timestamp}.png")
            plt.savefig(miss_path)
            plt.close()
            paths["missing"] = miss_path
        except Exception as e:
            print(f"❌ Failed to generate missing heatmap: {e}")

    return paths
