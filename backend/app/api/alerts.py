from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.db import get_db
from app.models.alert import AlertEvent, AlertRule
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["alerts"])

class AlertEventOut(BaseModel):
    id: UUID
    rule_id: UUID
    target_id: UUID
    triggered_at: datetime
    resolved_at: datetime | None
    triggering_value: float
    notified: bool

    class Config:
        from_attributes = True

@router.get("", response_model=list[AlertEventOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(AlertEvent).order_by(desc(AlertEvent.triggered_at)).limit(50).all()

@router.get("/active", response_model=list[AlertEventOut])
def active_alerts(db: Session = Depends(get_db)):
    return db.query(AlertEvent).filter(AlertEvent.resolved_at == None).order_by(desc(AlertEvent.triggered_at)).all()