import logging
from fastapi import APIRouter, HTTPException
from src.api.schemas.incident import IncidentInput
from src.services.analysis_service import analyze_incident
from src.services.prediction_service import predict_incident

router=APIRouter(tags=["analysis"])
logger=logging.getLogger(__name__)
@router.post("/analyze")
def analyze(payload: IncidentInput):
    try: return analyze_incident(payload.model_dump())
    except RuntimeError as exc: raise HTTPException(status_code=503,detail=str(exc)) from exc
    except Exception as exc: raise HTTPException(status_code=502,detail="Analysis provider or persistence unavailable; inspect server logs.") from exc
@router.post("/similar-incidents")
def similar(payload: IncidentInput):
    result=predict_incident(payload.model_dump())
    return {"incident_id":result["incident_id"],"similar_incidents":result["similar_incidents"]}
@router.post("/llm/summary")
def summary(payload: IncidentInput):
    try:
        result=predict_incident(payload.model_dump())
        from src.llm.gemini_client import GeminiProvider
        report=GeminiProvider().analyze(payload.model_dump(),result,result["extracted_entities"],result["similar_incidents"])
        return {"summary":report["summary"]}
    except Exception as exc:
        logger.exception("Gemini summary route failed")
        raise HTTPException(status_code=503,detail="Gemini analysis unavailable.") from exc
@router.post("/llm/investigation")
def investigation(payload: IncidentInput):
    try:
        result=predict_incident(payload.model_dump())
        from src.llm.gemini_client import GeminiProvider
        report=GeminiProvider().analyze(payload.model_dump(),result,result["extracted_entities"],result["similar_incidents"])
        return {"investigation_steps":report["investigation_steps"],"analysis":report}
    except Exception as exc:
        logger.exception("Gemini investigation route failed")
        raise HTTPException(status_code=503,detail="Gemini analysis unavailable.") from exc
@router.post("/llm/response")
def response(payload: IncidentInput):
    result=predict_incident(payload.model_dump())
    from src.llm.gemini_client import GeminiProvider
    report=GeminiProvider().analyze(payload.model_dump(),result,result["extracted_entities"],result["similar_incidents"])
    return {"recommended_actions":report["recommended_actions"],"analysis":report}
