import pandas as pd
import numpy as np
import re

# Simulate "df_articles_raw" with duplicate "PMU_P1" columns (e.g. from previous step)
df_articles_raw = pd.DataFrame({
    "ARTICOLO": ["A1"],
    "FAMIGLIA": ["F1"],
    "PMU_P1": [10],    # First column
    "PMU_P1_DUP": [20] # Second column (renamed manually for setup, but acts like dup)
})
df_articles_raw.columns = ["ARTICOLO", "FAMIGLIA", "PMU_P1", "PMU_P1"] # Force duplicate names
print("Source columns:", df_articles_raw.columns.tolist())

# Simulate CLIENT_RENAME and ARTICLE_RENAME
CLIENT_RENAME = {}
ARTICLE_RENAME = {
    "PMU_P1": "ARTICLE_PMU_P1", # This mapping is ambiguous if used in a dict
}

HELPER_KIND_COL = "_ROW_KIND"

def select_columns_handling_duplicates(df, target_cols):
    col_name_to_indices = {}
    for i, col in enumerate(df.columns):
        if col not in col_name_to_indices:
            col_name_to_indices[col] = []
        col_name_to_indices[col].append(i)
    
    indices_to_select = []
    usage_counts = {k: 0 for k in col_name_to_indices}
    
    for col in target_cols:
        if col in col_name_to_indices:
            available_indices = col_name_to_indices[col]
            count = usage_counts[col]
            if count < len(available_indices):
                indices_to_select.append(available_indices[count])
                usage_counts[col] += 1
            
    return df.iloc[:, indices_to_select]

# --- REPLICATE THE LOGIC ---
df_a = df_articles_raw.copy()

# 1. Manual Rename
new_cols = []
for col in df_a.columns:
    if col in ARTICLE_RENAME:
        new_cols.append(ARTICLE_RENAME[col])
    else:
        new_cols.append(col)
df_a.columns = new_cols
print("After manual rename:", df_a.columns.tolist())

# 2. Select
target_cols = ["ARTICOLO", "ARTICLE_PMU_P1", "ARTICLE_PMU_P1"] # Request duplicates
df_a = select_columns_handling_duplicates(df_a, target_cols)
print("After select:", df_a.columns.tolist())

# 3. Make Unique for Concat
def make_cols_unique(d):
    if d.columns.is_unique: return d
    cols = pd.Series(d.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [
            dup + (f".{i}" if i > 0 else "") 
            for i in range(sum(cols == dup))
        ]
    d.columns = cols
    return d

df_a = make_cols_unique(df_a)
print("After make unique:", df_a.columns.tolist())

# 4. Simulate Export (Restore)
df_export = df_a.copy()
df_export.columns = df_export.columns.str.replace(r"\.\d+$", "", regex=True)
print("Final Export Columns:", df_export.columns.tolist())

# Check values
print("Values:\n", df_export)
