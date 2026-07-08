from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import targets, metrics, alerts, rules

app = FastAPI(title="Homelab Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(targets.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(rules.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}