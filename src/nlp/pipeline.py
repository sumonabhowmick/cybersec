"""Run deterministic NLP extraction over cleaned incident descriptions."""
import json
import pandas as pd
from src.config.settings import DATA_PROCESSED, DATA_REPORTS
from src.nlp.entity_extractor import extract_entities

def run(path=DATA_PROCESSED/"cleaned_incidents.csv"):
    frame=pd.read_csv(path,low_memory=False)
    counts={}
    for text in frame["incident_text"].fillna(""):
        for kind, values in extract_entities(text).items(): counts[kind]=counts.get(kind,0)+len(values)
    target=DATA_REPORTS/"nlp_entity_counts.json"
    target.write_text(json.dumps({"records_analyzed":len(frame),"entity_counts":counts},indent=2),encoding="utf-8"); return target

if __name__=="__main__": print(run())
