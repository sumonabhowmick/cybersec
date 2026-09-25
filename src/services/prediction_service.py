"""Orchestrate model predictions, IOCs, ATT&CK references, and similarity."""
from __future__ import annotations
import uuid
from src.api.dependencies import get_models, get_similarity_engine
from src.nlp.entity_extractor import extract_entities
from src.models.predict import predict_one
from src.features.feature_schema import NUMERIC_FEATURES, CATEGORICAL_FEATURES

def predict_incident(incident: dict) -> dict:
    incident=dict(incident); incident["incident_id"]=incident.get("incident_id") or f"INC-{uuid.uuid4().hex[:12].upper()}"
    incident["incident_text"]=str(incident.get("incident_text", ""))
    for field in NUMERIC_FEATURES:
        incident.setdefault(field, None)
    for field in CATEGORICAL_FEATURES:
        incident.setdefault(field, None)
    models=get_models(); threat=predict_one(models["threat_category"],incident); severity=predict_one(models["severity_level"],incident)
    entities=extract_entities(incident["incident_text"])
    # Include explicitly supplied IOC-bearing fields while keeping extraction deterministic.
    entities_all=extract_entities(" ".join(str(incident.get(k,"")) for k in ["incident_text","source_ip","destination_ip","domain","url","file_name","file_hash","ioc_values","username","mitre_technique_id"]))
    for key, vals in entities.items(): entities_all[key]=sorted(set(entities_all.get(key,[])+vals))
    engine=get_similarity_engine(); similar=engine.search(incident["incident_text"],5,incident["incident_id"]) if engine else []
    return {"incident_id":incident["incident_id"],"threat_category":threat["label"],"threat_confidence":threat["confidence"],"threat_probabilities":threat["probabilities"],"severity_level":severity["label"],"severity_confidence":severity["confidence"],"severity_probabilities":severity["probabilities"],"top_factors":threat.get("top_factors",[]),"severity_top_factors":severity.get("top_factors",[]),"extracted_entities":entities_all,"mitre_information":{"techniques":entities_all.get("mitre_techniques",[]),"provided_technique":incident.get("mitre_technique_id"),"tactic":incident.get("mitre_tactic")},"similar_incidents":similar,"model_versions":{"threat_category":"local-selected-model","severity_level":"local-selected-model"}}
