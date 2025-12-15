import pandas as pd
import csv
from .utils import clean_column_names

HELPER_KIND_COL = "_ROW_KIND"
CLIENT_COLUMN_ORDER = [
    "CLIENTE", "CLIENT_CLUSTER", "MARGINE_LABEL", "VOLUME_LABEL",
    "FATTURATO_LABEL", "TENDENZA_LABEL", "CLIENT_N_VEND_P1",
    "CLIENT_KG_P1", "CLIENT_EUR_P1", "CLIENT_MARGINE",
    "CLIENT_VOLUME_DELTA", "CLIENT_FATTURATO_DELTA", "CLIENT_MARGINE_GAP"
]

ARTICLE_COLUMN_ORDER = [
    "ARTICOLO", "FAMIGLIA", "ARTICLE_LABEL", "ARTICLE_CLASS",
    "CLASSE_VENDITE", "CLASSE_KG", "ARTICLE_VENDITE", "ARTICLE_KG",
    "ARTICLE_EUR_P1", "ARTICLE_MARGINE", "QTA_P1", "PMU_P1"
]

CLIENT_RENAME = {
    "CLUSTER_LABEL": "CLIENT_CLUSTER",
    "MARGINE_PMU_P1": "CLIENT_MARGINE",
    "DIFF_KG_PREC_P1_P2": "CLIENT_VOLUME_DELTA",
    "DIFF_EUR_PREC_P1_P2": "CLIENT_FATTURATO_DELTA",
    "MARGINE_GAP_VS_KING": "CLIENT_MARGINE_GAP",
    "EUR_P1": "CLIENT_EUR_P1",
    "KG_P1": "CLIENT_KG_P1",
    "N_VEND_P1": "CLIENT_N_VEND_P1",
}

ARTICLE_RENAME = {
    "CLASSE_COMMERCIALE": "ARTICLE_CLASS",
    "ETICHETTA_COMMERCIALE": "ARTICLE_LABEL",
    "N_VEND_P1": "ARTICLE_VENDITE",
    "KG_P1": "ARTICLE_KG",
    "MARGINE_PMU_P1": "ARTICLE_MARGINE",
    "EUR_P1": "ARTICLE_EUR_P1",
    "QTA_P1": "ARTICLE_QTA_P1",
    "PMU_P1": "ARTICLE_PMU_P1",
}

def _existing_columns(df, candidates):
    return [c for c in candidates if c in df.columns]

def _reorder_columns(df):
    client_cols = _existing_columns(df, CLIENT_COLUMN_ORDER)
    article_cols = _existing_columns(df, ARTICLE_COLUMN_ORDER)
    remaining = [c for c in df.columns if c not in client_cols + article_cols + [HELPER_KIND_COL]]
    ordered = [HELPER_KIND_COL] + client_cols + article_cols + remaining
    return df.reindex(columns=ordered)

def process_unification(clients_path, articles_path, output_path_csv):
    print("🚀 Starting Unification...")
    
    # Load inputs
    if clients_path.endswith('.parquet'):
        df_clients = pd.read_parquet(clients_path)
    else:
        df_clients = pd.read_excel(clients_path)
    df_clients = clean_column_names(df_clients)
    
    if articles_path.endswith('.parquet'):
        df_articles = pd.read_parquet(articles_path)
    else:
        df_articles = pd.read_excel(articles_path)
    df_articles = clean_column_names(df_articles)
    
    # Build Unified Table
    df_c = df_clients.rename(columns=CLIENT_RENAME).copy()
    df_c[HELPER_KIND_COL] = "CLIENTE"
    df_c["ARTICOLO"] = ""
    df_c["FAMIGLIA"] = ""
    
    client_cols = [HELPER_KIND_COL, "CLIENTE", "ARTICOLO", "FAMIGLIA"] + list(CLIENT_RENAME.values()) + \
                  ["MARGINE_LABEL", "VOLUME_LABEL", "FATTURATO_LABEL", "TENDENZA_LABEL"]
    df_c = df_c[_existing_columns(df_c, client_cols)]

    df_a = df_articles.rename(columns=ARTICLE_RENAME).copy()
    df_a[HELPER_KIND_COL] = "ARTICOLO"
    df_a["CLIENTE"] = ""
    
    article_cols = [HELPER_KIND_COL, "CLIENTE", "ARTICOLO", "FAMIGLIA"] + list(ARTICLE_RENAME.values()) + \
                   ["CLASSE_VENDITE", "CLASSE_KG"]
    df_a = df_a[_existing_columns(df_a, article_cols)]

    all_cols = sorted(set(df_c.columns).union(df_a.columns))
    df_c = df_c.reindex(columns=all_cols)
    df_a = df_a.reindex(columns=all_cols)

    df_unified = pd.concat([df_c, df_a], ignore_index=True)
    df_unified = _reorder_columns(df_unified)

    # Remove TOTALE
    for col in ["CLIENTE", "ARTICOLO", "FAMIGLIA"]:
        if col in df_unified.columns:
            df_unified = df_unified[df_unified[col].astype(str).str.upper() != "TOTALE"]

    # Export
    export_df = df_unified.drop(columns=[HELPER_KIND_COL], errors="ignore")
    print(f"✅ Exporting to {output_path_csv}")
    export_df.to_csv(output_path_csv, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    
    return output_path_csv
