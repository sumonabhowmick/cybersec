"""Dependency accessors cached for API-process lifetime."""
from functools import lru_cache
from pathlib import Path
import json
from src.config.settings import MODEL_DIR, DATA_PROCESSED, DATA_REPORTS
from src.models.model_registry import load_artifact

@lru_cache(maxsize=1)
def get_models():
    result={}
    for target in ["threat_category","severity_level"]:
        path=MODEL_DIR/f"{target}.joblib"
        if path.exists(): result[target]=load_artifact(path)
    if len(result)!=2: raise RuntimeError("Trained models unavailable. Run python scripts/train_pipeline.py first.")
    return result

@lru_cache(maxsize=1)
def get_similarity_engine():
    path=MODEL_DIR/"similarity.joblib"
    if not path.exists(): return None
    return load_artifact(path)

def get_comparison_report():
    path=DATA_REPORTS/"model_comparison.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

@lru_cache(maxsize=1)
def get_overview():
    import pandas as pd
    path=DATA_PROCESSED/"cleaned_incidents.csv"
    if not path.exists(): return {"total_incidents":0,"high_critical":0,"threat_categories":0,"categories":[],"severity":[],"activity":[],"false_positive_rate":None,"average_response_time":None}
    frame=pd.read_csv(path,low_memory=False)
    severity=frame["severity_level"].fillna("Unknown").value_counts()
    categories=frame["threat_category"].fillna("Unknown").value_counts()
    timestamps=pd.to_datetime(frame["timestamp"],errors="coerce",utc=True)
    activity=timestamps.dt.date.value_counts().sort_index().tail(7)
    false_positive_rate=None
    if "false_positive" in frame:
        values=frame["false_positive"].astype("string").str.lower()
        known=values.isin(["yes","no","true","false"])
        if known.any(): false_positive_rate=float(values[known].isin(["yes","true"]).mean())
    response=pd.to_numeric(frame.get("response_time_minutes"),errors="coerce")
    return {"total_incidents":int(len(frame)),"high_critical":int(severity.reindex(["High","Critical"],fill_value=0).sum()),
        "threat_categories":int(frame["threat_category"].nunique()),
        "categories":[{"name":str(k),"count":int(v)} for k,v in categories.items()],
        "severity":[{"name":str(k),"count":int(v)} for k,v in severity.items()],
        "activity":[{"day":str(k),"value":int(v)} for k,v in activity.items()],
        "false_positive_rate":false_positive_rate,"average_response_time":float(response.mean()) if response.notna().any() else None}
