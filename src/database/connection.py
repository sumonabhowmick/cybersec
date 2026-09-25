"""Database connection factory."""
from src.config.settings import DATABASE

def connect():
    try: import psycopg2
    except ImportError as exc: raise RuntimeError("psycopg2 is not installed; install requirements.txt") from exc
    return psycopg2.connect(**DATABASE)
