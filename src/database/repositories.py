"""Small repository functions with transaction boundaries."""
from __future__ import annotations
import json
from src.database.connection import connect
from src.database import queries

def save_analysis(incident: dict, prediction: dict, entities: dict, similar: list, llm: dict | None = None) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(queries.INSERT_INCIDENT,(incident["incident_id"],incident.get("timestamp"),incident.get("incident_text",""),prediction["threat_category"],prediction["severity_level"],json.dumps(incident,default=str)))
        cur.execute(queries.INSERT_PREDICTION,(incident["incident_id"],prediction["threat_category"],prediction["threat_confidence"],prediction["severity_level"],prediction["severity_confidence"],json.dumps(prediction.get("model_versions",{}))))
        for kind, values in entities.items():
            for value in values: cur.execute("INSERT INTO extracted_entities (incident_id,entity_type,entity_value) VALUES (%s,%s,%s)",(incident["incident_id"],kind,value))
        for item in similar:
            cur.execute("INSERT INTO similar_incidents (incident_id,similar_incident_id,similarity_score) VALUES (%s,%s,%s)",(incident["incident_id"],item["incident_id"],item["similarity_score"]))
        if llm:
            cur.execute("INSERT INTO llm_analysis (incident_id,summary,investigation_guidance,recommended_response,model_name) VALUES (%s,%s,%s,%s,%s)",(incident["incident_id"],llm["summary"],json.dumps(llm["investigation_steps"]),json.dumps(llm["recommended_actions"]),"Gemini"))

def submit_feedback(payload: dict) -> int:
    values=(payload["incident_id"],payload.get("predicted_category"),payload.get("correct_category"),payload.get("predicted_severity"),payload.get("correct_severity"),payload.get("false_positive",False),payload.get("feedback",""),payload.get("analyst_id"))
    with connect() as conn, conn.cursor() as cur:
        cur.execute(queries.INSERT_FEEDBACK,values); return int(cur.fetchone()[0])

def list_incidents(limit=50,offset=0):
    with connect() as conn, conn.cursor() as cur:
        cur.execute(queries.LIST_INCIDENTS,(limit,offset)); rows=cur.fetchall()
    return [{"incident_id":r[0],"timestamp":r[1].isoformat() if r[1] else None,"threat_category":r[2],"severity_level":r[3],"payload":r[4]} for r in rows]

def get_incident(incident_id):
    with connect() as conn, conn.cursor() as cur: cur.execute(queries.GET_INCIDENT,(incident_id,)); row=cur.fetchone()
    return None if row is None else {"incident_id":row[0],"timestamp":row[1].isoformat() if row[1] else None,"incident_text":row[2],"threat_category":row[3],"severity_level":row[4],"payload":row[5]}
