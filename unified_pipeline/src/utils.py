import pandas as pd
import re

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names by stripping whitespace, replacing spaces with underscores,
    removing parentheses and special characters, and converting to uppercase.
    """
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "perc")
        .str.replace("/", "_")
        .str.replace("-", "_")
        .str.upper()
    )
    return df

def normalize_text(s):
    if pd.isna(s):
        return ""
    s = str(s).upper()
    s = re.sub(r"[^A-Z0-9]", "", s)
    return s
