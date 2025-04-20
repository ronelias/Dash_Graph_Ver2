import pandas as pd
import numpy as np
import re
import logging
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

logging.basicConfig(level=logging.INFO)

def is_likely_date(series: pd.Series) -> bool:
    """
    Heuristic to check if a column likely contains date strings.
    Looks for common formats like YYYY-MM-DD or YYYY/MM/DD.
    """
    if series.dropna().empty:
        return False

    sample = series.dropna().astype(str).head(20)
    date_pattern = r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$"
    return sample.str.match(date_pattern).mean() > 0.8


def load_csv_file(path: str) -> pd.DataFrame:
    """
    Load CSV file and automatically convert:
    - 0/1 columns to boolean
    - Date-like columns to datetime
    - Low-cardinality object columns to category
    """
    df = pd.read_csv(path, na_values=["", " ", "NA", "NaN", "nan", None])

    for col in df.columns:
        # Convert TRUE/FALSE strings
        if df[col].dtype == 'object':
            unique_vals = set(df[col].dropna().unique())
            if unique_vals.issubset({"TRUE", "FALSE"}):
                df[col] = df[col].map({"TRUE": True, "FALSE": False})

    # Convert 0/1 numeric to bool
    for col in df.columns:
        try:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) <= 2 and set(unique_vals).issubset({0, 1}):
                df[col] = df[col].astype(bool)
        except Exception as e:
            logging.warning(f"Bool detection failed for '{col}': {e}")

    # Convert likely date columns
    for col in df.columns:
        if df[col].dtype == 'object' and is_likely_date(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
            except Exception as e:
                logging.warning(f"Date conversion failed for '{col}': {e}")

    # Convert low-cardinality object columns to category
    for col in df.select_dtypes(include='object').columns:
        try:
            if df[col].nunique(dropna=True) < 30:
                df[col] = df[col].astype('category')
        except Exception as e:
            logging.warning(f"Category conversion failed for '{col}': {e}")

    return df


def display_dataframe(df: pd.DataFrame, table: QTableWidget, max_rows: int = 500) -> None:
    """
    Display a DataFrame in a PyQt5 QTableWidget. 
    Limits rows to max_rows to prevent UI slowdown.
    """
    rows_to_show = min(len(df), max_rows)

    if len(df) > max_rows:
        logging.info(f"Displaying only the first {max_rows} rows of {len(df)} total rows.")

    table.clear()
    table.setRowCount(rows_to_show)
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

    for row in range(rows_to_show):
        for col in range(df.shape[1]):
            value = df.iat[row, col]
            table.setItem(row, col, QTableWidgetItem(str(value)))


def apply_df_filter(df: pd.DataFrame, filter_expr: str) -> pd.DataFrame:
    """
    Apply a pandas query string to filter a DataFrame.
    """
    try:
        return df.query(filter_expr)
    except Exception as e:
        logging.error(f"Filter error: {e}")
        raise ValueError(f"Invalid filter expression: {filter_expr}") from e
