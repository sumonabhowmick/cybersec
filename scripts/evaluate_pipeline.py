"""Show final held-out results from the model comparison report."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.config.settings import DATA_REPORTS

if __name__=="__main__": print((DATA_REPORTS/"model_comparison.json").read_text(encoding="utf-8"))
