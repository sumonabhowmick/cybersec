CREATE INDEX IF NOT EXISTS idx_incidents_timestamp ON incidents(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_incidents_threat_category ON incidents(threat_category);
CREATE INDEX IF NOT EXISTS idx_incidents_severity_level ON incidents(severity_level);
CREATE INDEX IF NOT EXISTS idx_predictions_incident_id ON predictions(incident_id);
CREATE INDEX IF NOT EXISTS idx_entities_incident_id ON extracted_entities(incident_id);
CREATE INDEX IF NOT EXISTS idx_feedback_incident_id ON analyst_feedback(incident_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp DESC);
