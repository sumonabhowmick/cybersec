from fastapi import APIRouter
from src.api.dependencies import get_models

router=APIRouter(tags=["health"])
@router.get("/health")
def health():
    try: get_models(); models="ready"
    except Exception: models="unavailable"
    return {"status":"ok","models":models}
