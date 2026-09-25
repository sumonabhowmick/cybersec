"""Logistic regression candidate."""
from sklearn.linear_model import LogisticRegression

def build_baseline(seed=42):
    return LogisticRegression(max_iter=1200, class_weight="balanced", solver="lbfgs", random_state=seed)
