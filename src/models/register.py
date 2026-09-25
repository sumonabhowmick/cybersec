"""Register locally selected artifacts in MLflow when the registry is available."""
from src.config.settings import MLFLOW_TRACKING_URI, MODEL_DIR
import joblib

def register_all():
    try: import mlflow
    except ImportError as exc: raise RuntimeError("MLflow is not installed") from exc
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    for target in ["threat_category","severity_level"]:
        path=MODEL_DIR/f"{target}.joblib"
        if path.exists():
            pipeline=joblib.load(path)
            with mlflow.start_run(run_name=f"register-{target}"):
                info=mlflow.sklearn.log_model(pipeline,name="model",registered_model_name=f"cybersecurity-{target}",serialization_format="cloudpickle")
                print(f"Registered {target}: {info.model_uri}")

if __name__=="__main__": register_all()
