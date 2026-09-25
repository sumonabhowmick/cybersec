"""API smoke checks. Requires FastAPI and httpx from requirements.txt."""
import pytest

def test_health_endpoint_imports():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from src.api.main import app
    response=TestClient(app).get("/health")
    assert response.status_code==200
    assert "status" in response.json()
