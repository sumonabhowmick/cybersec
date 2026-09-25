"""Conservative cleaning that preserves security indicators and source data."""
from __future__ import annotations
import json, re
import ipaddress
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import pandas as pd
from src.config.settings import DATASET_PATH, DATA_PROCESSED, DATA_REPORTS
from src.data.validation import validate_frame

TEXT_COLUMNS = ["incident_text", "keywords", "named_entities", "ioc_values", "investigation_notes", "recommended_response", "resolution", "analyst_feedback"]
CAT_COLUMNS = ["threat_category", "severity_level", "priority", "threat_actor", "attack_vector", "event_source", "geographical_location", "protocol", "device_type", "affected_system", "asset_type", "asset_criticality", "business_impact", "mitre_tactic", "status", "false_positive", "ingestion_source_id"]
NUMERIC_COLUMNS = ["risk_score", "confidence_score", "source_port", "destination_port", "affected_users", "failed_login_attempts", "successful_login_attempts", "response_time_minutes", "word_count"]

def clean_frame(source: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    validate_frame(source)
    df = source.copy()
    start = len(df); missing_before = df.isna().sum().astype(int).to_dict()
    exact_duplicates = int(df.duplicated().sum()); df = df.drop_duplicates().copy()
    duplicate_ids = int(df["incident_id"].duplicated(keep="first").sum())
    df = df.drop_duplicates(subset=["incident_id"], keep="first").copy()
    corrections = {}
    for col in TEXT_COLUMNS:
        if col in df:
            before = df[col].fillna("").astype(str)
            normalized = before.str.replace(r"\s+", " ", regex=True).str.strip()
            corrections[col] = int((before != normalized).sum())
            df[col] = normalized.replace({"": pd.NA})
    for col in CAT_COLUMNS:
        if col in df:
            df[col] = df[col].astype("string").str.strip().replace("", pd.NA)
    invalid_iocs = 0
    for col in ["source_ip", "destination_ip"]:
        if col in df:
            def normalize_ip(value):
                nonlocal invalid_iocs
                if pd.isna(value) or not str(value).strip(): return pd.NA
                try: return ipaddress.ip_address(str(value).strip()).compressed.lower()
                except ValueError: invalid_iocs += 1; return pd.NA
            df[col] = df[col].map(normalize_ip).astype("string")
    if "domain" in df:
        df["domain"] = df["domain"].astype("string").str.strip().str.rstrip(".").str.lower().replace("", pd.NA)
    if "file_hash" in df:
        df["file_hash"] = df["file_hash"].astype("string").str.strip().str.lower().replace("", pd.NA)
    if "url" in df:
        def normalize_url(value):
            if pd.isna(value) or not str(value).strip(): return pd.NA
            raw=str(value).strip()
            try:
                parts=urlsplit(raw)
                if parts.scheme and parts.netloc:
                    return urlunsplit((parts.scheme.lower(),parts.netloc.lower(),parts.path,parts.query,parts.fragment))
            except ValueError: pass
            return raw
        df["url"] = df["url"].map(normalize_url).astype("string")
    if "username" in df: df["username"] = df["username"].astype("string").str.strip().replace("", pd.NA)
    if "mitre_technique_id" in df:
        df["mitre_technique_id"] = df["mitre_technique_id"].astype("string").str.upper().str.strip().replace("", pd.NA)
    if "ioc_values" in df:
        df["ioc_values"] = df["ioc_values"].astype("string").str.strip().replace("", pd.NA)
    for col in NUMERIC_COLUMNS:
        if col in df: df[col] = pd.to_numeric(df[col], errors="coerce")
    invalid_numeric = 0
    for col in ["source_port", "destination_port"]:
        if col in df:
            invalid = df[col].notna() & ~df[col].between(0, 65535)
            invalid_numeric += int(invalid.sum()); df.loc[invalid, col] = pd.NA
    for col in ["affected_users", "failed_login_attempts", "successful_login_attempts", "response_time_minutes", "risk_score", "word_count"]:
        if col in df:
            invalid = df[col].notna() & (df[col] < 0)
            invalid_numeric += int(invalid.sum()); df.loc[invalid, col] = pd.NA
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    rows_before_target_filter = len(df)
    df = df.dropna(subset=["incident_id", "timestamp", "incident_text", "threat_category", "severity_level"])
    report = {"initial_rows": start, "final_rows": int(len(df)), "exact_duplicates_removed": exact_duplicates,
        "duplicate_incident_ids_removed": duplicate_ids, "missing_values_before": {k:int(v) for k,v in missing_before.items()},
        "missing_values_after": {str(k):int(v) for k,v in df.isna().sum().items()}, "invalid_records": invalid_numeric,
        "corrected_values": corrections, "invalid_ip_values": invalid_iocs, "dropped_records": int(rows_before_target_filter-len(df)),
        "warnings": ["Rows with missing identity, timestamp, text, or target were dropped.", "Numeric missing values are retained for model-time imputation."]}
    return df.reset_index(drop=True), report

def clean_csv(source_path=DATASET_PATH, output_path=DATA_PROCESSED / "cleaned_incidents.csv"):
    df = pd.read_csv(source_path, low_memory=False)
    cleaned, report = clean_frame(df)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    (DATA_REPORTS / "cleaning_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return cleaned, report

if __name__ == "__main__":
    result, summary = clean_csv()
    print(f"Cleaned {len(result)} rows; report: {DATA_REPORTS / 'cleaning_report.json'}")
