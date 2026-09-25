"""Dataset validation and data quality reporting."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"incident_id", "timestamp", "incident_text", "threat_category", "severity_level"}
EXPECTED_COLUMNS = list("incident_id timestamp incident_text threat_category severity_level risk_score priority confidence_score threat_actor attack_vector event_source geographical_location source_ip destination_ip source_port destination_port protocol username device_type affected_system asset_type asset_criticality domain url file_name file_hash ioc_values named_entities keywords mitre_tactic mitre_technique_id business_impact affected_users failed_login_attempts successful_login_attempts recommended_response investigation_notes status resolution analyst_feedback false_positive response_time_minutes word_count predicted_threat_category topic_label ingestion_source_id".split())

def validate_frame(df: pd.DataFrame) -> dict:
    if df.empty:
        raise ValueError("CSV contains no incident rows; expected at least one row")
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")
    parsed = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    return {
        "rows": int(len(df)), "columns": int(len(df.columns)),
        "missing_expected_columns": sorted(set(EXPECTED_COLUMNS) - set(df.columns)),
        "unexpected_columns": sorted(set(df.columns) - set(EXPECTED_COLUMNS)),
        "duplicate_incident_ids": int(df["incident_id"].duplicated().sum()),
        "missing_incident_ids": int(df["incident_id"].isna().sum()),
        "invalid_timestamps": int(parsed.isna().sum()),
        "missing_by_column": {str(k): int(v) for k, v in df.isna().sum().items()},
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
    }

def validate_csv(path: str | Path, report_path: str | Path | None = None) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(path, low_memory=False)
    report = validate_frame(df)
    if report_path:
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        Path(report_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return df, report
