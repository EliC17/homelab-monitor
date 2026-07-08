from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.alert import AlertRule
from uuid import UUID
from pydantic import BaseModel

router = APIRouter(prefix="/rules", tags=["rules"])

class RuleCreate(BaseModel):
    target_id: UUID | None = None
    metric_name: str
    comparator: str
    threshold: float
    duration_s: int = 0
    severity: str = "warning"
    cooldown_s: int = 900
    enabled: bool = True

class RuleOut(RuleCreate):
    id: UUID

    class Config:
        from_attributes = True

@router.get("", response_model=list[RuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(AlertRule).all()

@router.post("", response_model=RuleOut, status_code=201)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    rule = AlertRule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.patch("/{rule_id}")
def update_rule(rule_id: UUID, payload: dict, db: Session = Depends(get_db)):
    rule = db.get(AlertRule, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    for key, value in payload.items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: UUID, db: Session = Depends(get_db)):
    rule = db.get(AlertRule, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    db.delete(rule)
    db.commit()