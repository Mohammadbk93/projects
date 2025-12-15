import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
from .utils import clean_column_names

def process_client_segmentation(input_path: str, output_path: str):
    print(f"🚀 Starting Client Segmentation...")
    print(f"   Input: {input_path}")

    # === Load files ===
    # Support both Excel and CSV/Parquet for input flexibility
    if input_path.endswith('.xlsx') or input_path.endswith('.xls'):
        df_clients = pd.read_excel(input_path, header=1)
    elif input_path.endswith('.csv'):
        df_clients = pd.read_csv(input_path)
    elif input_path.endswith('.parquet'):
        df_clients = pd.read_parquet(input_path)
    else:
        raise ValueError("Unsupported file format")

    # === Extract TOTALE row for benchmarks ===
    # Assuming 'CLIENTE' column exists before cleaning, or after?
    # The original script cleans *after* splitting, but 'CLIENTE' is used to split.
    # We might need to ensure the column name matches.
    # Let's clean first to be safe if columns are messy, but original script split first.
    # But original script accessed 'CLIENTE' directly.
    
    if 'CLIENTE' not in df_clients.columns:
        # Try cleaning first just in case
        df_clients = clean_column_names(df_clients)
    
    # Check again
    if 'CLIENTE' not in df_clients.columns:
         # Fallback if header=1 was wrong or something
         pass 

    df_totale = df_clients[df_clients['CLIENTE'] == "TOTALE"].copy()
    df_clients = df_clients[df_clients['CLIENTE'] != "TOTALE"]

    # === Normalize column names ===
    df_clients = clean_column_names(df_clients)
    df_totale = clean_column_names(df_totale)

    # === Extract King benchmarks automatically (from TOTALE row) ===
    try:
        king_avg_margine = df_totale["MARGINE_PMU_P1"].values[0]
        king_avg_volume = df_totale["DIFF_KG_PREC_P1_P2"].values[0]
        king_avg_fatturato = df_totale["DIFF_EUR_PREC_P1_P2"].values[0]
    except IndexError:
        print("⚠️ Warning: TOTALE row not found or empty. Using defaults or skipping benchmarks.")
        king_avg_margine = 0
        king_avg_volume = 0
        king_avg_fatturato = 0

    # === Classification Rules (Layer 1) ===
    def classify_margine(x, company_avg):
        diff = x - company_avg
        if -5 <= diff <= 5: return "Buono"
        elif 5.01 <= diff <= 10: return "Alto"
        elif diff > 10.01: return "Ottimo"
        elif -10 <= diff <= -5.1: return "Basso"
        else: return "Molto basso"

    def classify_volume(x):
        if 0 <= x <= 5: return "Buono"
        elif x > 5: return "Ottimo"
        elif -5 <= x < 0: return "Stabile"
        elif -10 <= x < -5: return "In calo"
        else: return "Critico"

    def classify_fatturato(x):
        if 0.01 <= x <= 5: return "Buono"
        elif x > 5: return "Ottimo"
        elif -10 <= x <= 0: return "Stabile"
        elif -15 <= x < -10: return "In calo"
        else: return "Critico"

    def classify_tendenza(x):
        if -3 <= x <= 3: return "Buono"
        elif x < -3.1: return "Scarso"
        else: return "Ottimo"

    # Apply rule-based segmentation
    df_clients["Margine_Label"] = df_clients["MARGINE_PMU_P1"].apply(lambda v: classify_margine(v, king_avg_margine))
    df_clients["Margine_Gap_vs_King"] = df_clients["MARGINE_PMU_P1"] - king_avg_margine
    df_clients["Volume_Label"] = df_clients["DIFF_KG_PREC_P1_P2"].apply(classify_volume)
    df_clients["Fatturato_Label"] = df_clients["DIFF_EUR_PREC_P1_P2"].apply(classify_fatturato)
    df_clients["Tendenza_Label"] = (df_clients["MARGINE_PMU_P1"] - df_clients["MARGINE_PMU_P2"]).apply(classify_tendenza)

    # === K-Means Clustering (Layer 2) ===
    features = ["KG_P1", "EUR_P1", "MARGINE_PMU_P1", "DIFF_KG_PREC_P1_P2", "DIFF_EUR_PREC_P1_P2"]
    
    # Ensure features exist
    missing_features = [f for f in features if f not in df_clients.columns]
    if missing_features:
        print(f"⚠️ Missing features for clustering: {missing_features}")
        # Handle or skip clustering? Assuming input is correct for now.
    
    X = df_clients[features].copy()
    X = X.fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df_clients["Cluster_ID"] = kmeans.fit_predict(X_scaled)

    cluster_names = {
        0: "Clienti Strategici (Alto Volume & Alto Fatturato)",
        1: "Volume Alto, Margine Basso",
        2: "Clienti Emergenti (Crescita Positiva)",
        3: "Nicchia Profittevole (Margine Alto, Volume Limitato)",
        4: "Clienti in Calo (Trend Negativo)"
    }

    df_clients["Cluster_Label"] = df_clients["Cluster_ID"].map(cluster_names)

    # === Merge back TOTALE row for reference ===
    df_final = pd.concat([df_totale, df_clients], ignore_index=True)

    # === Keep only selected columns ===
    selected_cols = [
        "CLIENTE",
        "N_VEND_P1", "KG_P1", "EUR_P1", "MARGINE_PMU_P1",
        "DIFF_KG_PREC_P1_P2", "DIFF_EUR_PREC_P1_P2",
        "N_VEND_P2", "KG_P2", "EUR_P2", "MARGINE_PMU_P2",
        "Margine_Gap_vs_King", "Margine_Label", "Volume_Label",
        "Fatturato_Label", "Tendenza_Label",
        "Cluster_Label"
    ]

    df_final = df_final[[c for c in selected_cols if c in df_final.columns]]

    # === Export ===
    # Use Parquet for internal pipeline efficiency
    print(f"✅ Exporting to {output_path}")
    df_final.to_parquet(output_path, index=False)
    
    return output_path
