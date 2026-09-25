"""Importable ASGI app compatibility entrypoint."""
from src.api.main import app

__all__=["app"]

if __name__=="__main__":
    import os, uvicorn
    uvicorn.run("src.api.main:app",host=os.getenv("API_HOST","127.0.0.1"),port=int(os.getenv("API_PORT","8000")))
