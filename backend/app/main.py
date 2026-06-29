from fastapi import FastAPI
from app.api import targets
 
app = FastAPI(title="Homelab Monitor API")
app.include_router(targets.router, prefix="/api/v1")
 
@app.get("/health")
def health():
    return {"status": "ok"}
