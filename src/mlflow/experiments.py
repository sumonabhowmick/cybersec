"""Experiment metadata helpers."""
from src.mlflow.tracking import configure_tracking

def active_experiment(): return configure_tracking().active_run()
