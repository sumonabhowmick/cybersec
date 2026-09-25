import pytest
from src.llm.safety import parse_json_response

def test_rejects_malformed_response():
    with pytest.raises(ValueError): parse_json_response("not json")

def test_accepts_structured_response():
    value={"summary":"s","investigation_steps":[],"recommended_actions":[],"risk_notes":[],"model_explanation":"m"}
    assert parse_json_response(__import__("json").dumps(value))["summary"]=="s"
