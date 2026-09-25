"""Full prediction and analyst-assistance orchestration."""
from src.services.prediction_service import predict_incident
from src.llm.gemini_client import GeminiProvider
from src.database.repositories import save_analysis
import logging

logger=logging.getLogger(__name__)

def analyze_incident(incident: dict) -> dict:
    result=predict_incident(incident)
    evidence=dict(incident); evidence["incident_id"]=result["incident_id"]
    try:
        llm=GeminiProvider().analyze(evidence,result,result["extracted_entities"],result["similar_incidents"])
        llm_status="available"
    except Exception:
        logger.exception("Gemini assistance unavailable for incident %s",result["incident_id"])
        llm={"summary":"Gemini assistance is unavailable. The ML prediction is still available for analyst review.",
            "investigation_steps":[],"recommended_actions":[],"risk_notes":[],"model_explanation":"See model confidence and top factors; do not treat this prediction as a confirmed incident."}
        llm_status="unavailable"
    save_analysis(evidence,result,result["extracted_entities"],result["similar_incidents"],llm if llm_status=="available" else None)
    return {"prediction":result,"llm_analysis":llm,"llm_status":llm_status}
