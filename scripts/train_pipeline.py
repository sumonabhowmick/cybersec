"""Run ingestion validation, cleaning, schema export, similarity fit, and model comparison."""
from __future__ import annotations
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.config.settings import DATASET_PATH, DATA_PROCESSED, MODEL_DIR
from src.data.ingestion import ingest
from src.data.cleaning import clean_csv
from src.features.feature_schema import write_schema
from src.models.train import train_all
from src.similarity.tfidf_engine import SimilarityEngine
import pandas as pd

def main():
    ingest(DATASET_PATH)
    cleaned, report=clean_csv(DATASET_PATH)
    write_schema(DATA_PROCESSED/"feature_schema.json")
    engine=SimilarityEngine().fit(cleaned)
    engine.save(MODEL_DIR/"similarity.joblib")
    metrics=train_all(DATA_PROCESSED/"cleaned_incidents.csv")
    print(json.dumps({"rows":len(cleaned),"cleaning":report,"selected_models":{k:v["selected_model"] for k,v in metrics.items()}},indent=2,default=str))

if __name__=="__main__": main()
