"""Classification metrics with stable class labels and confusion matrix."""
from __future__ import annotations
import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def evaluate_model(model, X, y, labels=None) -> dict:
    started = time.perf_counter(); pred = model.predict(X); elapsed = (time.perf_counter()-started)/max(1, len(y))
    labels = list(labels) if labels is not None else sorted(set(y))
    return {"accuracy": float(accuracy_score(y,pred)), "precision_macro": float(precision_score(y,pred,average="macro",zero_division=0)),
        "recall_macro": float(recall_score(y,pred,average="macro",zero_division=0)), "macro_f1": float(f1_score(y,pred,average="macro",zero_division=0)),
        "weighted_f1": float(f1_score(y,pred,average="weighted",zero_division=0)), "inference_time_per_row_seconds": float(elapsed),
        "confusion_matrix": confusion_matrix(y,pred,labels=labels).tolist(), "labels": labels,
        "classification_report": classification_report(y,pred,labels=labels,output_dict=True,zero_division=0)}

if __name__=="__main__":
    from src.config.settings import DATA_REPORTS
    report=DATA_REPORTS/"model_comparison.json"
    if not report.exists(): raise SystemExit("No results yet. Run python scripts/train_pipeline.py first.")
    print(report.read_text(encoding="utf-8"))
