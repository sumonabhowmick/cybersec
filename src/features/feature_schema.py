"""Explicit ingestion-time and excluded-field policy."""
from __future__ import annotations
import json
from pathlib import Path

NUMERIC_FEATURES = ["risk_score", "affected_users", "failed_login_attempts", "successful_login_attempts", "source_port", "destination_port", "word_count"]
CATEGORICAL_FEATURES = ["attack_vector", "event_source", "geographical_location", "threat_actor", "device_type", "affected_system", "asset_type", "asset_criticality", "protocol", "business_impact", "mitre_tactic", "mitre_technique_id", "ingestion_source_id"]
TEXT_FEATURES = ["incident_text"]
TARGETS = ["threat_category", "severity_level"]
POST_INCIDENT = ["recommended_response", "investigation_notes", "resolution", "analyst_feedback", "false_positive", "status", "response_time_minutes", "predicted_threat_category", "topic_label"]
LEAKAGE_PRONE = ["priority", "confidence_score"]
IDENTIFIERS_AND_UNVALIDATED = ["incident_id", "timestamp", "source_ip", "destination_ip", "username", "domain", "url", "file_name", "file_hash", "ioc_values", "named_entities", "keywords"]

def schema() -> dict:
    return {"available_at_ingestion": NUMERIC_FEATURES + CATEGORICAL_FEATURES + TEXT_FEATURES,
            "generated_during_preprocessing": ["TF-IDF n-grams from incident_text", "numeric median imputation", "categorical most-frequent imputation and one-hot encoding"],
            "targets": TARGETS, "post_incident_excluded": POST_INCIDENT,
            "leakage_prone_excluded": LEAKAGE_PRONE,
            "identifier_or_sensitive_excluded": IDENTIFIERS_AND_UNVALIDATED,
            "policy": "Only fields known at ingestion with defensible prediction-time availability are used. Audit availability before production."}

def write_schema(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(schema(), indent=2), encoding="utf-8")
