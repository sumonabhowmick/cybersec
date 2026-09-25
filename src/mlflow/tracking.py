"""Small wrapper for MLflow tracking initialization."""
from src.config.settings import MLFLOW_TRACKING_URI

def configure_tracking(experiment="cybersecurity-incident-classification"):
    try: import mlflow
    except ImportError as exc: raise RuntimeError("MLflow is not installed; install requirements.txt") from exc
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI); mlflow.set_experiment(experiment)
    return mlflow
