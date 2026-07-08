from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import targets, alerts, rules, auth
from app.api.metrics import collector_router, metrics_router
from app.api.auth import get_current_user
from app.core.config import settings

app = FastAPI(title="Homelab Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_collector_auth(x_collector_secret: str = Header(...)):
    if x_collector_secret != settings.collector_secret:
        raise HTTPException(403, "Invalid collector secret")

# public
app.include_router(auth.router, prefix="/api/v1")

# collector-facing (shared secret)
app.include_router(collector_router, prefix="/api/v1",
    dependencies=[Depends(get_collector_auth)])

# browser-facing (JWT)
app.include_router(targets.router, prefix="/api/v1",
    dependencies=[Depends(get_current_user)])
app.include_router(metrics_router, prefix="/api/v1",
    dependencies=[Depends(get_current_user)])
app.include_router(alerts.router, prefix="/api/v1",
    dependencies=[Depends(get_current_user)])
app.include_router(rules.router, prefix="/api/v1",
    dependencies=[Depends(get_current_user)])

@app.get("/health")
def health():
    return {"status": "ok"}