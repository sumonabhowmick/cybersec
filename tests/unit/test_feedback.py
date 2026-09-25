from src.services import feedback_service

def test_feedback_repository_result_is_returned(monkeypatch):
    monkeypatch.setattr(feedback_service,"submit_feedback",lambda payload:17)
    assert feedback_service.record_feedback({"incident_id":"i-1"})==17
