"""Local artifact registry helpers (MLflow is the authoritative experiment registry)."""
from __future__ import annotations
from pathlib import Path
import joblib, json

def save_artifact(model, metadata: dict, name: str, directory: str | Path):
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    path=directory/f"{name}.joblib"; joblib.dump(model,path)
    (directory/f"{name}.json").write_text(json.dumps(metadata,indent=2,default=str),encoding="utf-8")
    return path

def load_artifact(path): return joblib.load(path)
