"""Apply ordered SQL migrations to an existing PostgreSQL database."""
from pathlib import Path
from src.database.connection import connect

def migrate():
    migration_dir=Path(__file__).resolve().parents[1]/"migrations"
    with connect() as conn, conn.cursor() as cur:
        for path in sorted(migration_dir.glob("*.sql")):
            cur.execute(path.read_text(encoding="utf-8"))
            print(f"Applied {path.name}")

if __name__=="__main__": migrate()
