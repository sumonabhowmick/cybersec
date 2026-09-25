"""Generate dataset summaries and Plotly distribution charts."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from src.config.settings import DATA_PROCESSED, REPORTS

COLUMNS = ["threat_category", "severity_level", "priority", "attack_vector", "device_type", "asset_type", "asset_criticality", "mitre_tactic", "mitre_technique_id", "event_source", "business_impact", "false_positive", "geographical_location"]

def run_eda(path=DATA_PROCESSED / "cleaned_incidents.csv", output_dir=REPORTS / "eda"):
    import plotly.express as px
    df = pd.read_csv(path, low_memory=False); output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    summary = {c: df[c].fillna("Unknown").value_counts().head(30).to_dict() for c in COLUMNS if c in df}
    for col in ["risk_score", "confidence_score", "affected_users", "failed_login_attempts", "successful_login_attempts", "response_time_minutes", "word_count"]:
        if col in df: summary[col] = df[col].describe().replace({float('nan'):None}).to_dict()
    (output_dir / "eda_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    for col in COLUMNS:
        if col in df:
            counts = df[col].fillna("Unknown").value_counts().head(30).rename_axis(col).reset_index(name="count")
            px.bar(counts, x=col, y="count", title=f"Incident distribution: {col}").write_html(output_dir / f"{col}.html", include_plotlyjs="cdn")
    for col in ["risk_score", "confidence_score", "response_time_minutes", "word_count"]:
        if col in df: px.histogram(df, x=col, title=f"Distribution: {col}").write_html(output_dir / f"{col}_histogram.html", include_plotlyjs="cdn")
    return summary

if __name__ == "__main__": run_eda()
