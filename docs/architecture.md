# Architecture

The system has four independently usable layers: CSV/cleaning and EDA, classical NLP and a leakage-controlled sklearn classification pipeline, FastAPI services, and a React analyst console. PostgreSQL persists reviewed analysis and feedback. MLflow records training runs; Gemini supplies analyst-oriented text only.

```mermaid
flowchart LR
  CSV[Immutable source CSV] --> ING[Validation and cleaning]
  ING --> FEAT[TF-IDF + structured features]
  FEAT --> TRAIN[Threat and severity model comparison]
  TRAIN --> ART[Selected pipelines and model report]
  ART --> API[FastAPI]
  API --> SIM[TF-IDF cosine retrieval]
  API --> GEM[Gemini analyst assistance]
  API --> PG[(PostgreSQL)]
  API --> UI[React SOC dashboard]
  UI --> FB[Human feedback]
  FB --> PG
  TRAIN --> MLF[MLflow]
```

Model outputs and LLM recommendations are separate fields and display areas. Authentication is an integration point, not implemented; bind to a trusted network and add organizational authentication before deployment.
