"""Optional XGBoost candidate, loaded only when installed."""
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder

class EncodedXGBClassifier(BaseEstimator, ClassifierMixin):
    """Translate arbitrary string labels to the integer labels XGBoost expects."""
    def __init__(self, **params): self.params=params
    def fit(self, X, y):
        from xgboost import XGBClassifier
        self.encoder_=LabelEncoder().fit(y)
        self.model_=XGBClassifier(**self.params)
        self.model_.fit(X,self.encoder_.transform(y)); self.classes_=self.encoder_.classes_
        return self
    def predict(self,X): return self.encoder_.inverse_transform(self.model_.predict(X).astype(int))
    def predict_proba(self,X): return self.model_.predict_proba(X)
    def get_params(self,deep=True): return {"params":self.params}
    def set_params(self,**params): self.params.update(params); return self

def build_xgboost(seed=42, **overrides):
    try: import xgboost  # noqa: F401
    except ImportError as exc: raise RuntimeError("XGBoost is not installed. Install requirements.txt to enable this candidate.") from exc
    config = {"n_estimators":300,"max_depth":8,"learning_rate":0.08,"subsample":0.9,"colsample_bytree":0.9,"min_child_weight":2,"objective":"multi:softprob","eval_metric":"mlogloss","tree_method":"hist","n_jobs":-1,"random_state":seed}
    config.update(overrides); return EncodedXGBClassifier(**config)
