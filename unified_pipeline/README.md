# Unified Data Pipeline

This project unifies client segmentation, SKU mapping, and article segmentation into a single pipeline.

## Structure

- `src/`: Contains the logic for each step of the pipeline.
- `main.py`: The orchestrator that runs the steps in order.
- `data/`: Place your input Excel files here.
- `output/`: The pipeline results will be saved here (intermediate Parquet files and final CSV).

## Usage with Docker

1. Build the image:
   ```bash
   docker build -t unified-pipeline .
   ```

2. Run the pipeline (mounting data):
   ```bash
   docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output unified-pipeline
   ```

## Pipeline Steps

1. **Client Segmentation**: Processes client data, applies classification rules and clustering. Outputs `clients_segmented.parquet`.
2. **SKU Mapping**: Maps sales data to catalog using exact and fuzzy matching. Outputs `sku_mapped.parquet`.
3. **Article Segmentation**: Filters mapped articles by family and applies business rules. Outputs `articles_segmented.parquet`.
4. **Unification**: Combines client and article data into a single CSV for PowerBI. Outputs `unified_output.csv`.

## Configuration

You can override input paths using arguments:
```bash
python main.py --client-file /path/to/file.xlsx
```
