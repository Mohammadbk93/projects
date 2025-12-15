import os
import argparse
from src.client_segmentation import process_client_segmentation
from src.sku_mapping import process_sku_mapping
from src.article_segmentation import process_article_segmentation
from src.unification import process_unification

def main():
    parser = argparse.ArgumentParser(description="Unified Data Pipeline")
    
    # Input files
    parser.add_argument("--client-file", default=os.getenv("CLIENT_FILE", "data/ANALISI_VEND_CLIENTE_31.10.25.xlsx"))
    parser.add_argument("--sales-file", default=os.getenv("SALES_FILE", "data/ANALISI_VEND_ART_31.10.25.xlsx"))
    parser.add_argument("--catalog-file", default=os.getenv("CATALOG_FILE", "data/articoli KING.xlsx"))
    parser.add_argument("--families-file", default=os.getenv("FAMILIES_FILE", "data/famiglie_da_includere.xlsx"))
    
    # Output directory
    parser.add_argument("--output-dir", default=os.getenv("OUTPUT_DIR", "output"))
    
    # Step selection
    parser.add_argument("--step", choices=["all", "clients", "sku", "articles", "unify"], default="all", help="Which step to run")

    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Define intermediate paths
    client_segmented_path = os.path.join(args.output_dir, "clients_segmented.parquet")
    sku_mapped_path = os.path.join(args.output_dir, "sku_mapped.parquet")
    articles_segmented_path = os.path.join(args.output_dir, "articles_segmented.parquet")
    final_output_path = os.path.join(args.output_dir, "unified_output.csv")
    
    # Step 1: Client Segmentation
    if args.step in ["all", "clients"]:
        try:
            process_client_segmentation(args.client_file, client_segmented_path)
        except Exception as e:
            print(f"❌ Step 1 (Clients) failed: {e}")
            return

    # Step 2: SKU Mapping
    if args.step in ["all", "sku"]:
        try:
            process_sku_mapping(args.sales_file, args.catalog_file, sku_mapped_path)
        except Exception as e:
            print(f"❌ Step 2 (SKU) failed: {e}")
            return

    # Step 3: Article Segmentation
    if args.step in ["all", "articles"]:
        # Ensure input exists if running standalone
        if not os.path.exists(sku_mapped_path) and args.step == "articles":
            print(f"❌ Missing input: {sku_mapped_path}. Run --step sku first.")
            return

        try:
            process_article_segmentation(sku_mapped_path, args.families_file, articles_segmented_path)
        except Exception as e:
            print(f"❌ Step 3 (Articles) failed: {e}")
            return

    # Step 4: Unification
    if args.step in ["all", "unify"]:
        # Ensure inputs exist
        if (not os.path.exists(client_segmented_path) or not os.path.exists(articles_segmented_path)) and args.step == "unify":
             print(f"❌ Missing inputs. Ensure client and article steps are complete.")
             return

        try:
            process_unification(client_segmented_path, articles_segmented_path, final_output_path)
        except Exception as e:
            print(f"❌ Step 4 (Unification) failed: {e}")
            return
        
    print(f"✨ Selected steps ({args.step}) completed successfully!")

if __name__ == "__main__":
    main()
