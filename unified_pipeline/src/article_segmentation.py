import pandas as pd
import re
from .utils import clean_column_names, normalize_text

def process_article_segmentation(mapped_path, families_path, output_path):
    print("🚀 Starting Article Segmentation...")
    
    # Load mapped data (likely Parquet)
    if mapped_path.endswith('.parquet'):
        df = pd.read_parquet(mapped_path)
    else:
        df = pd.read_excel(mapped_path) if mapped_path.endswith('.xlsx') else pd.read_csv(mapped_path)
        
    df = clean_column_names(df)
    
    # Load families
    if families_path.endswith('.xlsx'):
        df_famiglie = pd.read_excel(families_path)
    else:
        df_famiglie = pd.read_csv(families_path)
    
    df_famiglie = clean_column_names(df_famiglie)
    
    if "FAMIGLIA" not in df_famiglie.columns:
        raise ValueError("FAMIGLIA column missing in families file")
        
    famiglie_poc_raw = df_famiglie["FAMIGLIA"].dropna().astype(str).str.strip().tolist()
    famiglie_poc_clean = [normalize_text(f) for f in famiglie_poc_raw]
    
    df["FAMIGLIA_NORM"] = df["FAMIGLIA"].apply(normalize_text)
    
    mask_totale = df["ARTICOLO"].astype(str).str.upper().str.contains("TOTALE", na=False)
    df_totale = df[mask_totale]
    
    df_main = df[df["FAMIGLIA_NORM"].isin(famiglie_poc_clean)]
    
    keep_cols = ["ARTICOLO", "FAMIGLIA", "N_VEND_P1", "KG_P1", "MARGINE_PMU_P1", "EUR_P1", "QTA_P1", "PMU_P1"]
    df_main = df_main[[col for col in keep_cols if col in df.columns]]
    df_totale = df_totale[[col for col in keep_cols if col in df.columns]]
    
    # Thresholds
    THRESHOLDS = {
        "N_VEND_P1": {"low": 10, "high": 47},
        "KG_P1": {"low": 86, "high": 734}
    }
    
    def classify_vendite(x):
        if x > THRESHOLDS["N_VEND_P1"]["high"]: return "X"
        elif x >= THRESHOLDS["N_VEND_P1"]["low"]: return "Y"
        else: return "Z"

    def classify_kg(x):
        if x > THRESHOLDS["KG_P1"]["high"]: return "A"
        elif x >= THRESHOLDS["KG_P1"]["low"]: return "B"
        else: return "C"

    df_main["CLASSE_VENDITE"] = df_main["N_VEND_P1"].apply(classify_vendite)
    df_main["CLASSE_KG"] = df_main["KG_P1"].apply(classify_kg)
    
    def combine_classes(row):
        combo = f"{row['CLASSE_VENDITE']}_{row['CLASSE_KG']}"
        if combo in ["X_A", "X_B", "Y_A", "Z_A"]:
            return 1, "Alta rilevanza commerciale"
        elif combo in ["X_C", "Y_B"]:
            return 2, "Media rilevanza commerciale"
        else:
            return 3, "Bassa rilevanza commerciale"
            
    df_main[["CLASSE_COMMERCIALE", "ETICHETTA_COMMERCIALE"]] = pd.DataFrame(
        df_main.apply(combine_classes, axis=1).tolist(),
        index=df_main.index,
        columns=["CLASSE_COMMERCIALE", "ETICHETTA_COMMERCIALE"]
    )
    
    df_final = pd.concat([df_totale, df_main], ignore_index=True)
    
    print(f"✅ Exporting to {output_path}")
    df_final.to_parquet(output_path, index=False)
    
    return output_path
