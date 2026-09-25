# Feature policy

The model uses incident text, risk score, affected user count, login counts, source/destination ports, word count, and documented categorical fields known at ingestion (attack vector, event source, geography, actor, device, affected system, asset type/criticality, protocol, business impact, MITRE tactic/technique, ingestion source). Derived login ratios, total attempts, and selected port indicators are computed before fitting.

Targets: `threat_category`, `severity_level`. Leakage-prone and excluded: `priority`, `confidence_score`, `status`, `response_time_minutes`. Post-incident and excluded: predicted category, topic, recommended response, investigation notes, resolution, analyst feedback, false-positive label. Identifiers and raw IOC fields are excluded pending governance review. Structured-field availability must be confirmed for the intended production ingestion time.
