from pydantic import BaseModel
from src.api.schemas.prediction import PredictionResponse

class AnalysisResponse(BaseModel):
    prediction: PredictionResponse
    llm_analysis: dict
