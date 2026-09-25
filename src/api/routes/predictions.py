from fastapi import APIRouter, HTTPException
from src.api.schemas.incident import IncidentInput
from src.services.prediction_service import predict_incident

router=APIRouter(tags=["predictions"])
@router.post("/predict")
def predict(payload: IncidentInput):
    try: return predict_incident(payload.model_dump())
    except RuntimeError as exc: raise HTTPException(status_code=503,detail=str(exc)) from exc
    except Exception as exc: raise HTTPException(status_code=500,detail="Prediction failed; inspect server logs.") from exc
