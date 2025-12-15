import pandas as pd
import re
from rapidfuzz import process, fuzz
import numpy as np
from .utils import normalize_text, clean_column_names

def normalize_code_enhanced(code):
    if pd.isna(code):
        return ["", "", "", ""]
    
    code_str = str(code).upper().strip()
    
    clean1 = re.sub(r"[^A-Z0-9\-_]", "", code_str)
    clean2 = re.sub(r"[^A-Z0-9]", "", code_str)
    clean3 = code_str.replace("O", "0").replace("I", "1").replace("S", "5").replace("B", "8")
    clean3 = re.sub(r"[^A-Z0-9]", "", clean3)
    clean4 = re.sub(r"^0+", "", clean2)
    
    return [clean1, clean2, clean3, clean4]

def normalize_descr_enhanced(text):
    if pd.isna(text):
        return ""
    text_str = str(text).upper().strip()
    clean = re.sub(r"[^A-Z0-9\s]", "", text_str)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

class AdvancedSKUMatcher:
    def __init__(self, catalog_df):
        self.catalog = catalog_df.copy()
        self.prepare_catalog()
        
    def prepare_catalog(self):
        print("🔧 Preparing catalog...")
        self.catalog["COD_CLEAN_1"] = self.catalog["COD.KING"].apply(lambda x: normalize_code_enhanced(x)[0])
        self.catalog["COD_CLEAN_2"] = self.catalog["COD.KING"].apply(lambda x: normalize_code_enhanced(x)[1])
        self.catalog["COD_CLEAN_3"] = self.catalog["COD.KING"].apply(lambda x: normalize_code_enhanced(x)[2])
        self.catalog["COD_CLEAN_4"] = self.catalog["COD.KING"].apply(lambda x: normalize_code_enhanced(x)[3])
        
        self.catalog["DESCRIZ_CLEAN"] = self.catalog["DESCRIZ."].apply(normalize_descr_enhanced)
        self.catalog["DESCRIZ_ORIG"] = self.catalog["DESCRIZ."]
        self.catalog = self.catalog.drop_duplicates(subset=["COD_CLEAN_1"], keep="first")
        
    def build_mapping_dictionaries(self):
        self.mappings = {}
        self.mappings["conservative"] = dict(zip(self.catalog["COD_CLEAN_1"], self.catalog["DESCRIZ_ORIG"]))
        self.mappings["aggressive"] = dict(zip(self.catalog["COD_CLEAN_2"], self.catalog["DESCRIZ_ORIG"]))
        self.mappings["ocr_corrected"] = dict(zip(self.catalog["COD_CLEAN_3"], self.catalog["DESCRIZ_ORIG"]))
        self.mappings["no_leading_zeros"] = dict(zip(self.catalog["COD_CLEAN_4"], self.catalog["DESCRIZ_ORIG"]))
        
    def exact_match(self, sales_df):
        print("🎯 Performing exact matching...")
        sales_df["FAMIGLIA"] = None
        sales_df["MATCH_STRATEGY"] = None
        sales_df["MATCH_CONFIDENCE"] = None
        
        strategies = ["conservative", "aggressive", "ocr_corrected", "no_leading_zeros"]
        
        for strategy in strategies:
            if strategy == "conservative":
                sales_df["ARTICOLO_CLEAN"] = sales_df["ARTICOLO"].apply(lambda x: normalize_code_enhanced(x)[0])
            elif strategy == "aggressive":
                sales_df["ARTICOLO_CLEAN"] = sales_df["ARTICOLO"].apply(lambda x: normalize_code_enhanced(x)[1])
            elif strategy == "ocr_corrected":
                sales_df["ARTICOLO_CLEAN"] = sales_df["ARTICOLO"].apply(lambda x: normalize_code_enhanced(x)[2])
            elif strategy == "no_leading_zeros":
                sales_df["ARTICOLO_CLEAN"] = sales_df["ARTICOLO"].apply(lambda x: normalize_code_enhanced(x)[3])
            
            unmatched_mask = sales_df["FAMIGLIA"].isna()
            matches = sales_df.loc[unmatched_mask, "ARTICOLO_CLEAN"].map(self.mappings[strategy])
            
            new_matches = matches.notna()
            sales_df.loc[unmatched_mask & new_matches, "FAMIGLIA"] = matches[new_matches]
            sales_df.loc[unmatched_mask & new_matches, "MATCH_STRATEGY"] = strategy
            sales_df.loc[unmatched_mask & new_matches, "MATCH_CONFIDENCE"] = 100
        
        return sales_df
    
    def fuzzy_match(self, sales_df, score_cutoff=85):
        print(f"🔍 Performing fuzzy matching (score ≥ {score_cutoff})...")
        unmatched_mask = sales_df["FAMIGLIA"].isna()
        unmatched_codes = sales_df.loc[unmatched_mask, "ARTICOLO_CLEAN"].unique()
        
        if len(unmatched_codes) == 0:
            return sales_df
        
        catalog_codes = self.catalog["COD_CLEAN_2"].tolist()
        code_to_descr = dict(zip(self.catalog["COD_CLEAN_2"], self.catalog["DESCRIZ_ORIG"]))
        
        def find_fuzzy_match(code):
            if not code: return None, None, None
            
            best_match, best_score, best_algorithm = None, 0, None
            
            for scorer, name in [(fuzz.partial_ratio, "partial_ratio"), 
                                 (fuzz.token_set_ratio, "token_set_ratio"), 
                                 (fuzz.ratio, "ratio")]:
                res = process.extractOne(code, catalog_codes, scorer=scorer, score_cutoff=score_cutoff)
                if res and res[1] > best_score:
                    best_match, best_score, best_algorithm = res[0], res[1], name
            
            if best_match:
                return code_to_descr[best_match], best_score, f"fuzzy_{best_algorithm}"
            return None, None, None
        
        fuzzy_results = {}
        for code in unmatched_codes:
            descr, score, algorithm = find_fuzzy_match(code)
            if descr:
                fuzzy_results[code] = (descr, score, algorithm)
        
        for code, (descr, score, algorithm) in fuzzy_results.items():
            mask = (sales_df["ARTICOLO_CLEAN"] == code) & sales_df["FAMIGLIA"].isna()
            sales_df.loc[mask, "FAMIGLIA"] = descr
            sales_df.loc[mask, "MATCH_STRATEGY"] = algorithm
            sales_df.loc[mask, "MATCH_CONFIDENCE"] = score
            
        return sales_df
    
    def partial_match(self, sales_df):
        print("🔍 Performing partial matching...")
        unmatched_mask = sales_df["FAMIGLIA"].isna()
        unmatched_codes = sales_df.loc[unmatched_mask, "ARTICOLO_CLEAN"].unique()
        
        if len(unmatched_codes) == 0: return sales_df
        
        code_to_descr = dict(zip(self.catalog["COD_CLEAN_2"], self.catalog["DESCRIZ_ORIG"]))
        
        for code in unmatched_codes:
            if not code or len(code) < 4: continue
            
            variations = [code[:-1], code[:-2], code[1:], code[2:]]
            for variation in variations:
                if variation in code_to_descr:
                    mask = (sales_df["ARTICOLO_CLEAN"] == code) & sales_df["FAMIGLIA"].isna()
                    sales_df.loc[mask, "FAMIGLIA"] = code_to_descr[variation]
                    sales_df.loc[mask, "MATCH_STRATEGY"] = "partial_match"
                    sales_df.loc[mask, "MATCH_CONFIDENCE"] = 90
                    break
        return sales_df

def process_sku_mapping(sales_path, catalog_path, output_path):
    print(f"🚀 Starting SKU Mapping...")
    
    # Load
    if sales_path.endswith('.xlsx'):
        sales = pd.read_excel(sales_path, header=1)
    else:
        sales = pd.read_parquet(sales_path) if sales_path.endswith('.parquet') else pd.read_csv(sales_path)
        
    if catalog_path.endswith('.xlsx'):
        catalog = pd.read_excel(catalog_path)
    else:
        catalog = pd.read_parquet(catalog_path) if catalog_path.endswith('.parquet') else pd.read_csv(catalog_path)
    
    # Clean column names
    sales.columns = sales.columns.str.strip().str.upper()
    catalog.columns = catalog.columns.str.strip().str.upper()
    
    # Matcher
    matcher = AdvancedSKUMatcher(catalog)
    matcher.build_mapping_dictionaries()
    
    sales = matcher.exact_match(sales)
    sales = matcher.fuzzy_match(sales, score_cutoff=80)
    sales = matcher.partial_match(sales)
    
    # Special cases
    sales.loc[
        sales["ARTICOLO"].astype(str).str.upper().str.contains("TOTALE", na=False),
        ["FAMIGLIA", "MATCH_STRATEGY", "MATCH_CONFIDENCE"]
    ] = ["TOTALE", "special_case", 100]
    
    sales["FAMIGLIA"] = sales["FAMIGLIA"].fillna("Unknown")
    sales["MATCH_STRATEGY"] = sales["MATCH_STRATEGY"].fillna("no_match")
    
    print(f"✅ Exporting to {output_path}")
    sales.to_parquet(output_path, index=False)
    
    return output_path
