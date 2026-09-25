from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class IncidentInput(BaseModel):
    model_config=ConfigDict(extra="allow")
    incident_id: str | None = Field(default=None,max_length=128)
    timestamp: datetime | None = None
    incident_text: str = Field(min_length=5,max_length=20000)
    risk_score: float | None = Field(default=None,ge=0)
    affected_users: int | None = Field(default=None,ge=0)
    failed_login_attempts: int | None = Field(default=None,ge=0)
    successful_login_attempts: int | None = Field(default=None,ge=0)
    source_port: int | None = Field(default=None,ge=0,le=65535)
    destination_port: int | None = Field(default=None,ge=0,le=65535)
    word_count: int | None = Field(default=None,ge=0)
