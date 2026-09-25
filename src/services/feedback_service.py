"""Human-reviewed feedback persistence; does not retrain production models."""
from src.database.repositories import submit_feedback

def record_feedback(payload: dict) -> int: return submit_feedback(payload)
