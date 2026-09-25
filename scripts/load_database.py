"""Apply PostgreSQL migrations."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from database.seed.seed_database import migrate

if __name__=="__main__": migrate()
