"""FastAPI application with centralized safe error responses and request auditing."""
from __future__ import annotations
import logging, os, time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import health, incidents, predictions, analysis, feedback, models

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger("cybersec.api")
app=FastAPI(title="Cybersecurity Incident Intelligence API",version="1.0.0",description="ML incident classification with human-supervised analyst assistance")
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["GET","POST"],allow_headers=["*"])
for route in [health.router,incidents.router,predictions.router,analysis.router,feedback.router,models.router]: app.include_router(route)

@app.middleware("http")
async def request_log(request:Request,call_next):
    started=time.perf_counter(); response=None
    try:
        response=await call_next(request)
        return response
    finally:
        elapsed=(time.perf_counter()-started)*1000
        status=getattr(response,"status_code",500)
        logger.info("%s %s -> %s (%.1fms)",request.method,request.url.path,status,elapsed)
        if request.url.path != "/health":
            try:
                from src.database.connection import connect
                with connect() as conn, conn.cursor() as cur:
                    cur.execute("INSERT INTO audit_logs (user_id,action,endpoint,status,details) VALUES (%s,%s,%s,%s,%s::jsonb)",("anonymous",request.method,request.url.path,str(status),'{"source":"api","latency_ms":'+str(round(elapsed,1))+'}'))
            except Exception:
                logger.debug("Audit persistence unavailable",exc_info=True)

@app.exception_handler(Exception)
async def safe_exception_handler(request:Request,exc:Exception):
    logger.exception("Unhandled request failure at %s",request.url.path)
    return JSONResponse(status_code=500,content={"detail":"Internal server error"})
