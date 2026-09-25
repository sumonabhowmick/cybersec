# PostgreSQL

Create a database named `cybersecurity_db`, configure `.env`, then run `python scripts/load_database.py`. Ordered SQL migrations create incidents, predictions, entities, similarity, LLM analysis, analyst feedback, model metadata, audit logs, and indexes. All values use psycopg2 parameters. Feedback is retained for review and does not trigger automatic training.
