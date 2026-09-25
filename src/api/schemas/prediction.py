from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    incident_id: str
    threat_category: str
    threat_confidence: float
    threat_probabilities: dict[str, float] = Field(default_factory=dict)
    severity_level: str
    severity_confidence: float
    severity_probabilities: dict[str, float] = Field(default_factory=dict)
    top_factors: list[str] = Field(default_factory=list)
    extracted_entities: dict
    mitre_information: dict
    similar_incidents: list
    model_versions: dict
