from fastapi import APIRouter, HTTPException, Query
from src.api.schemas.incident import IncidentInput
from src.services.incident_service import list_incidents, get_incident
from src.database.connection import connect
from src.database.queries import INSERT_INCIDENT
import json

router=APIRouter(tags=["incidents"])
@router.post("/incidents")
def create_incident(payload: IncidentInput):
    data=payload.model_dump(mode="json"); incident_id=data.get("incident_id") or "INC-"+__import__("uuid").uuid4().hex[:12].upper()
    with connect() as conn, conn.cursor() as cur:
        cur.execute(INSERT_INCIDENT,(incident_id,data.get("timestamp"),data["incident_text"],None,None,json.dumps(data)))
    return {"incident_id":incident_id,"status":"created"}
@router.get("/incidents")
def incidents(limit:int=Query(50,ge=1,le=500),offset:int=Query(0,ge=0)):
    try: return {"items":list_incidents(limit,offset),"limit":limit,"offset":offset}
    except Exception as exc: raise HTTPException(503,"Database unavailable") from exc
@router.get("/incidents/{incident_id}")
def incident(incident_id:str):
    result=get_incident(incident_id)
    if result is None: raise HTTPException(404,"Incident not found")
    return result
