"""Central configuration with workspace-relative paths and environment secrets."""
from __future__ import annotations

import os
from pathlib import Path
try:
    from dotenv import load_dotenv
except ImportError:  # Core data tooling remains usable before installing API extras.
    def load_dotenv(*args, **kwargs):
        return False

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_REPORTS = ROOT / "data" / "reports"
REPORTS = ROOT / "reports"
MODEL_DIR = ROOT / "models" / "artifacts"
RANDOM_SEED = 42
DATASET_PATH = Path(os.getenv("DATASET_PATH", str(DATA_RAW / "cybersecurity_incidents_10000_final.csv")))
DATABASE = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", "5432")),
    "dbname": os.getenv("DATABASE_NAME", "cybersecurity_db"),
    "user": os.getenv("DATABASE_USER", "postgres"),
    "password": os.getenv("DATABASE_PASSWORD", ""),
}
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.7-flash")

for _path in (DATA_RAW, DATA_PROCESSED, DATA_REPORTS, MODEL_DIR, REPORTS):
    _path.mkdir(parents=True, exist_ok=True)
