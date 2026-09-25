"""Reusable sparse TF-IDF construction helpers."""
from sklearn.feature_extraction.text import TfidfVectorizer

def make_vectorizer(max_features: int = 20000, ngram_range: tuple[int,int] = (1,2)) -> TfidfVectorizer:
    return TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, min_df=2, sublinear_tf=True, token_pattern=r"(?u)\b[\w./:@+-]+\b")
