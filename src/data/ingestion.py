"""Read the immutable source CSV and emit data quality diagnostics."""
from __future__ import annotations
import logging
from src.config.settings import DATASET_PATH, DATA_REPORTS
from src.data.validation import validate_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

def ingest(path=DATASET_PATH):
    df, report = validate_csv(path, DATA_REPORTS / "data_quality_report.json")
    logging.info("Read %d rows from %s", len(df), path)
    return df, report

if __name__ == "__main__":
    _, quality = ingest()
    print(f"Validated {quality['rows']} rows; report: {DATA_REPORTS / 'data_quality_report.json'}")
