# API

Run `python run.py`; OpenAPI docs appear at `/docs`. Routes include `GET /health`, `POST /incidents`, `GET /incidents`, `GET /incidents/{incident_id}`, `POST /predict`, `POST /analyze`, `POST /similar-incidents`, `POST /feedback`, `GET /models`, `GET /metrics`, `GET /audit-logs`, and analyst-assistance routes under `/llm/`. Model artifacts are required for prediction. Full analysis also requires Gemini and PostgreSQL.
