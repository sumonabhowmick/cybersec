from fastapi import APIRouter, HTTPException
from src.api.schemas.feedback import FeedbackInput
from src.services.feedback_service import record_feedback

router=APIRouter(tags=["feedback"])
@router.post("/feedback")
def feedback(payload:FeedbackInput):
    try: return {"feedback_id":record_feedback(payload.model_dump()),"status":"recorded_for_review"}
    except Exception as exc: raise HTTPException(503,"Feedback storage unavailable") from exc
