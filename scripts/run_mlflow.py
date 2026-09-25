"""Start the local MLflow tracking UI."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.config.settings import MLFLOW_TRACKING_URI

if __name__=="__main__": raise SystemExit(subprocess.call([sys.executable,"-m","mlflow","ui","--backend-store-uri",MLFLOW_TRACKING_URI]))
