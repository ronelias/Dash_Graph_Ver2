import pandas as pd
from typing import Dict, Any

def compute_eda_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the DataFrame and return key statistics and summaries for report generation.
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "types": {
            "numerical": list(df.select_dtypes(include="number").columns),
            "categorical": list(df.select_dtypes(include=["object", "category"]).columns),
            "boolean": list(df.select_dtypes(include="bool").columns),
            "datetime": list(df.select_dtypes(include="datetime").columns),
        },
        "describe": df.describe().T,
        "missing": df.isnull().mean().sort_values(ascending=False),
        "skew": df.select_dtypes(include="number").skew(),
        "cardinality": {
            col: df[col].nunique() for col in df.select_dtypes(include=["object", "category"])
        },
        "constant_cols": [col for col in df.columns if df[col].nunique() == 1],
        "top_categories": {
            col: df[col].value_counts().head() for col in df.select_dtypes(include="object").columns[:3]
        },
    }
