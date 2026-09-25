"""Random forest candidate."""
from sklearn.ensemble import RandomForestClassifier

def build_random_forest(seed=42, **overrides):
    config = {"n_estimators":300,"max_depth":24,"min_samples_split":2,"min_samples_leaf":1,"max_features":"sqrt","class_weight":"balanced_subsample","n_jobs":-1,"random_state":seed}
    config.update(overrides); return RandomForestClassifier(**config)
