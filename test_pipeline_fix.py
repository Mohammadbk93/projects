import pandas as pd
import re

# ... (Previous imports and setup)

# [Helper to allow duplicate column selection]
def select_columns_allow_duplicates(df, target_cols):
    """
    Selects columns from df matching target_cols.
    If a column in target_cols appears multiple times in df, selects all instances.
    If a column in target_cols appears once in df but multiple times in target_cols list,
    it duplicates the column in the output.
    """
    selected = []
    # Create a frequency map of requested columns
    # target_cols can have duplicates like ['A', 'B', 'B']
    
    # Simple approach: iterate through target_cols and pick from df
    # But we need to handle if df has duplicates itself?
    # Case A: df has ['A', 'B'] and we want ['A', 'B', 'B'] -> Select A, B, and B again?
    # Case B: df has ['A', 'B', 'B'] and we want ['A', 'B', 'B'] -> Select A, B(1), B(2)
    
    # The user's specific case is likely Case B:
    # "PMU_P1" is in the dataframe twice (from previous step).
    # And "PMU_P1" is in the requested list twice.
    
    # 1. Identify available columns in DF (handling duplicates by index)
    df_cols = list(df.columns)
    
    # 2. Build a list of indices to select
    indices_to_select = []
    
    # We need to map requested names to actual column indices
    # If "PMU_P1" is requested twice, and exists twice at indices 10 and 11:
    #   Request 1 -> Index 10
    #   Request 2 -> Index 11
    
    # Helper map: Name -> list of indices
    name_to_indices = {}
    for idx, name in enumerate(df_cols):
        if name not in name_to_indices:
            name_to_indices[name] = []
        name_to_indices[name].append(idx)
        
    # Track which index of the duplicate we used last
    name_usage_count = {} 
    
    final_col_names = []
    
    for target in target_cols:
        if target in name_to_indices:
            available_indices = name_to_indices[target]
            count = name_usage_count.get(target, 0)
            
            # If we have more requests than available columns, recycle the last one? 
            # Or just take what is available?
            # User said: "I have that duplication... I want to have both columns"
            # Assuming 1-to-1 mapping if counts match.
            
            if count < len(available_indices):
                idx = available_indices[count]
                indices_to_select.append(idx)
                final_col_names.append(target)
                name_usage_count[target] = count + 1
            else:
                # We requested it more times than it exists? 
                # (e.g. requested 3 times, exists 2). 
                # Or maybe we just skip?
                pass
                
    return df.iloc[:, indices_to_select]


def build_unified_table(df_clients_raw: pd.DataFrame, df_articles_raw: pd.DataFrame) -> pd.DataFrame:
    # ... (Renaming logic) ...
    # Instead of dictionary renaming which merges duplicates, we must handle carefully.
    
    # 1. Rename columns in df_articles_raw
    # If df_articles_raw has [..., "PMU_P1", "PMU_P1"], simply applying .rename might be tricky
    # dictionary rename: {"PMU_P1": "ARTICLE_PMU_P1"} -> both become "ARTICLE_PMU_P1"
    
    df_a = df_articles_raw.copy()
    
    # Custom renaming to preserve structure
    new_cols = []
    for col in df_a.columns:
        if col in ARTICLE_RENAME:
            new_cols.append(ARTICLE_RENAME[col])
        else:
            new_cols.append(col)
    df_a.columns = new_cols
    
    # Now df_a has [..., "ARTICLE_PMU_P1", "ARTICLE_PMU_P1"]
    
    df_a[HELPER_KIND_COL] = "ARTICOLO"
    df_a["CLIENTE"] = ""
    
    article_cols_target = [
        HELPER_KIND_COL,
        "CLIENTE",
        "ARTICOLO",
        "FAMIGLIA",
        "ARTICLE_VENDITE",
        "ARTICLE_KG",
        "ARTICLE_EUR_P1",
        "ARTICLE_MARGINE",
        "CLASSE_VENDITE",
        "CLASSE_KG",
        "ARTICLE_CLASS",
        "ARTICLE_LABEL",
        "ARTICLE_QTA_P1",
        "ARTICLE_PMU_P1",
        "ARTICLE_PMU_P1", # Requested twice
    ]
    
    # Custom selection function
    df_a = select_columns_allow_duplicates(df_a, article_cols_target)

    # ... (Rest of logic)
