import os
from typing import Optional
import pandas as pd

from eda_logic import compute_eda_insights
from eda_plots import save_eda_plots
from eda_report import generate_html_report

def run_eda(df: pd.DataFrame, output_dir: Optional[str] = "eda_reports") -> str:
    """
    Orchestrates the EDA workflow:
    - Computes insights from the DataFrame
    - Generates visual plots (correlation, missing values)
    - Creates a styled HTML report using GPT summarization

    Parameters:
        df (pd.DataFrame): The dataset to analyze.
        output_dir (str): Where to save the plots and report.

    Returns:
        str: Path to the generated HTML report.
    """
    os.makedirs(output_dir, exist_ok=True)

    insights = compute_eda_insights(df)
    plots = save_eda_plots(df, output_dir)
    return generate_html_report(insights, plots, output_dir)
