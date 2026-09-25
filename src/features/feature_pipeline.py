"""Build the leakage-safe sparse feature transformer."""
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.features.feature_schema import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from src.features.structured_features import add_derived_features

DERIVED_NUMERIC = ["total_login_attempts", "login_failure_ratio", "login_success_ratio", "source_port_risk_indicator", "destination_port_risk_indicator"]

def build_feature_transformer(max_features: int = 20000, ngram_range: tuple[int,int] = (1,2)) -> Pipeline:
    numeric = Pipeline([("impute", SimpleImputer(strategy="median", add_indicator=True)), ("scale", StandardScaler(with_mean=False))])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=2))])
    columns = ColumnTransformer([
        ("text", TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, min_df=2, sublinear_tf=True, token_pattern=r"(?u)\b[\w./:@+-]+\b"), "incident_text"),
        ("numeric", numeric, NUMERIC_FEATURES + DERIVED_NUMERIC),
        ("categorical", categorical, CATEGORICAL_FEATURES),
    ], remainder="drop", sparse_threshold=1.0)
    return Pipeline([("derive", _DerivedTransformer()), ("features", columns)])

class _DerivedTransformer:
    def fit(self, X, y=None): return self
    def transform(self, X): return add_derived_features(X)
    def get_params(self, deep=True): return {}
    def set_params(self, **params): return self
