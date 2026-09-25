import numpy as np
from src.models.evaluate import evaluate_model

class _Model:
    def predict(self,X): return np.array(["a","b"])

def test_metrics_include_macro_f1_and_confusion_matrix():
    result=evaluate_model(_Model(),[1,2],["a","b"])
    assert result["macro_f1"]==1
    assert result["confusion_matrix"]==[[1,0],[0,1]]
