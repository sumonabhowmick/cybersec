"""End-to-end model and Gemini analysis requires trained artifacts and service credentials."""
import os
import pytest

@pytest.mark.skipif(os.getenv("RUN_END_TO_END")!="1",reason="Requires trained models, PostgreSQL, and Gemini configuration")
def test_analysis_pipeline():
    from src.services.analysis_service import analyze_incident
    report=analyze_incident({"incident_text":"Suspicious credential access from 8.8.8.8", "incident_id":"TEST-1"})
    assert "prediction" in report and "llm_analysis" in report
