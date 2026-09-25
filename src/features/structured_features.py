"""Derived prediction-time numeric indicators from incident input."""
from __future__ import annotations
import pandas as pd
from src.nlp.entity_extractor import extract_entities

def add_derived_features(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    for column in ["failed_login_attempts", "successful_login_attempts", "source_port", "destination_port"]:
        if column not in df: df[column] = 0
    failed = pd.to_numeric(df["failed_login_attempts"], errors="coerce").fillna(0)
    success = pd.to_numeric(df["successful_login_attempts"], errors="coerce").fillna(0)
    df["total_login_attempts"] = failed + success
    df["login_failure_ratio"] = failed.div(df["total_login_attempts"].replace(0, 1))
    df["login_success_ratio"] = success.div(df["total_login_attempts"].replace(0, 1))
    for column, name in [("source_port", "source"), ("destination_port", "destination")]:
        port = pd.to_numeric(df[column], errors="coerce")
        df[f"{name}_port_risk_indicator"] = port.isin([21,22,23,25,445,1433,3389,4444,5900,8080]).astype(int)
    return df
