import pandas as pd
from src.similarity.tfidf_engine import SimilarityEngine

def test_similarity_excludes_requested_incident():
    frame=pd.DataFrame([{"incident_id":"a","incident_text":"phishing email credential theft","threat_category":"Phishing"},{"incident_id":"b","incident_text":"phishing email credential theft","threat_category":"Phishing"}])
    engine=SimilarityEngine().fit(frame)
    results=engine.search("phishing email",top_k=5,exclude_incident_id="a")
    assert [x["incident_id"] for x in results]==["b"]
