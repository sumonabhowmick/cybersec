"""Fit and persist training-corpus TF-IDF for analyst-oriented retrieval."""
from __future__ import annotations
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:
    def __init__(self, max_features: int = 20000):
        self.vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1,2), min_df=1, sublinear_tf=True, token_pattern=r"(?u)\b[\w./:@+-]+\b")
        self.matrix = None; self.records = None
    def fit(self, records):
        self.records = records.reset_index(drop=True).copy()
        self.matrix = self.vectorizer.fit_transform(self.records["incident_text"].fillna("").astype(str))
        return self
    def search(self, text: str, top_k: int = 5, exclude_incident_id: str | None = None) -> list[dict]:
        if self.matrix is None: return []
        scores = cosine_similarity(self.vectorizer.transform([text]), self.matrix).ravel()
        order = scores.argsort()[::-1]
        results = []
        for idx in order:
            row = self.records.iloc[idx]
            if exclude_incident_id and str(row.get("incident_id")) == str(exclude_incident_id): continue
            results.append({"incident_id": str(row.get("incident_id", "")), "similarity_score": float(scores[idx]),
                "threat_category": str(row.get("threat_category", "")), "severity_level": str(row.get("severity_level", "")),
                "timestamp": str(row.get("timestamp", "")), "attack_vector": str(row.get("attack_vector", "")),
                "mitre_technique_id": str(row.get("mitre_technique_id", ""))})
            if len(results) >= max(0, top_k): break
        return results
    def save(self, path): joblib.dump(self, path)
    @classmethod
    def load(cls, path): return joblib.load(path)
