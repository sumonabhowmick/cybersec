from fastapi import APIRouter
from src.api.dependencies import get_comparison_report, get_overview

router=APIRouter(tags=["models"])
@router.get("/overview")
def overview(): return get_overview()
@router.get("/models")
def models(): return get_comparison_report()
@router.get("/metrics")
def metrics(): return get_comparison_report()
@router.get("/audit-logs")
def audit_logs(limit:int=100):
    from src.database.connection import connect
    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT user_id,action,endpoint,timestamp,status,details FROM audit_logs ORDER BY timestamp DESC LIMIT %s",(min(max(limit,1),500),)); rows=cur.fetchall()
    return {"items":[{"user_id":r[0],"action":r[1],"endpoint":r[2],"timestamp":r[3].isoformat(),"status":r[4],"details":r[5]} for r in rows]}
