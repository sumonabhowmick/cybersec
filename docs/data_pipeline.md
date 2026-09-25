# Data pipeline

`src.data.ingestion` reads the configured CSV without editing it and writes `data/reports/data_quality_report.json`. `src.data.cleaning` removes exact and repeated IDs, conservatively normalizes text/categorical values, validates ports and nonnegative counts, and saves a new processed CSV plus a cleaning report. Missing numeric values are retained for training-time imputation. Rows without identity, timestamp, text, or target are removed.

The original input is stored under `data/raw/`; set `DATASET_PATH` to use a different location. The feature policy explicitly separates ingestion-time features from post-incident and leakage-prone fields.
