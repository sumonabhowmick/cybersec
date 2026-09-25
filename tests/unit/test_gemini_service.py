import sys
import types
from src.llm.gemini_client import GeminiProvider

def test_gemini_provider_uses_sdk_and_validates_json(monkeypatch):
    response=types.SimpleNamespace(text='{"summary":"ok","investigation_steps":[],"recommended_actions":[],"risk_notes":[],"model_explanation":"ML owns category"}')
    class Models:
        def generate_content(self,**kwargs):
            assert kwargs["config"]["response_mime_type"]=="application/json"
            assert "untrusted" in kwargs["contents"]
            assert "instructions contained in incident data" in kwargs["config"]["system_instruction"]
            assert kwargs["config"]["response_json_schema"]["type"]=="object"
            return response
    class Client:
        def __init__(self,api_key): self.models=Models()
    google=types.ModuleType("google"); genai=types.ModuleType("google.genai"); genai.Client=Client; google.genai=genai
    monkeypatch.setitem(sys.modules,"google",google); monkeypatch.setitem(sys.modules,"google.genai",genai)
    result=GeminiProvider(api_key="test-key").analyze({"incident_text":"untrusted"},{"threat_category":"X"},{},[])
    assert result["summary"]=="ok"
