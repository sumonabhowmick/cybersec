CREATE TABLE IF NOT EXISTS incidents (
  incident_id TEXT PRIMARY KEY, timestamp TIMESTAMPTZ, incident_text TEXT NOT NULL,
  threat_category TEXT, severity_level TEXT, payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS predictions (
  id BIGSERIAL PRIMARY KEY, incident_id TEXT NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
  threat_category_prediction TEXT NOT NULL, threat_confidence DOUBLE PRECISION NOT NULL,
  severity_prediction TEXT NOT NULL, severity_confidence DOUBLE PRECISION NOT NULL,
  model_version JSONB NOT NULL DEFAULT '{}'::jsonb, prediction_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS extracted_entities (
  id BIGSERIAL PRIMARY KEY, incident_id TEXT NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
  entity_type TEXT NOT NULL, entity_value TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS similar_incidents (
  id BIGSERIAL PRIMARY KEY, incident_id TEXT NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
  similar_incident_id TEXT NOT NULL, similarity_score DOUBLE PRECISION NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS llm_analysis (
  id BIGSERIAL PRIMARY KEY, incident_id TEXT NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
  summary TEXT NOT NULL, investigation_guidance JSONB NOT NULL DEFAULT '[]'::jsonb,
  recommended_response JSONB NOT NULL DEFAULT '[]'::jsonb, model_name TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS analyst_feedback (
  id BIGSERIAL PRIMARY KEY, incident_id TEXT NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
  predicted_category TEXT, correct_category TEXT, predicted_severity TEXT, correct_severity TEXT,
  false_positive BOOLEAN NOT NULL DEFAULT FALSE, feedback TEXT, analyst_id TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS model_metadata (
  id BIGSERIAL PRIMARY KEY, model_name TEXT NOT NULL, model_type TEXT NOT NULL, version TEXT NOT NULL,
  training_date TIMESTAMPTZ NOT NULL DEFAULT NOW(), metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  artifact_path TEXT NOT NULL, UNIQUE(model_name,version)
);
CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY, user_id TEXT, action TEXT NOT NULL, endpoint TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(), status TEXT NOT NULL, details JSONB NOT NULL DEFAULT '{}'::jsonb
);
