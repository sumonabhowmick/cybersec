"""Public similarity search facade."""
from src.similarity.tfidf_engine import SimilarityEngine

def find_similar(engine: SimilarityEngine, text: str, top_k: int = 5, exclude_incident_id=None):
    return engine.search(text, top_k=top_k, exclude_incident_id=exclude_incident_id)
