from pydantic import BaseModel, Field

class FeedbackInput(BaseModel):
    incident_id: str
    predicted_category: str | None = None
    correct_category: str | None = None
    predicted_severity: str | None = None
    correct_severity: str | None = None
    false_positive: bool = False
    feedback: str = Field(default="",max_length=4000)
    analyst_id: str | None = Field(default=None,max_length=128)
