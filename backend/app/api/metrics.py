from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.db import get_db
from app.models.metric import MetricSample
from app.schemas.metric import MetricIngest, MetricOut
from app.models.alert import AlertRule
from app.services.evaluator import evaluate_rule
from uuid import UUID

# collector-facing routes (protected by collector secret in main.py)
collector_router = APIRouter(tags=["collector"])

@collector_router.get("/internal/targets")
def internal_targets(db: Session = Depends(get_db)):
    from app.models.target import Target
    return db.query(Target).filter(Target.enabled == True).all()

@collector_router.post("/metrics/ingest", status_code=201)
def ingest(payload: list[MetricIngest], db: Session = Depends(get_db)):
    rows = [MetricSample(**m.model_dump()) for m in payload]
    db.bulk_save_objects(rows)
    db.commit()
    for row in rows:
        rules = (db.query(AlertRule)
            .filter(
                AlertRule.metric_name == row.metric_name,
                AlertRule.enabled == True,
            )
            .filter(
                (AlertRule.target_id == None) |
                (AlertRule.target_id == row.target_id)
            )
            .all())
        for rule in rules:
            evaluate_rule(db, rule, row)
    return {"ingested": len(rows)}

# browser-facing routes (protected by JWT in main.py)
metrics_router = APIRouter(tags=["metrics"])

@metrics_router.get("/targets/{target_id}/metrics", response_model=list[MetricOut])
def get_metrics(
    target_id: UUID,
    metric_name: str | None = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    q = db.query(MetricSample).filter(MetricSample.target_id == target_id)
    if metric_name:
        q = q.filter(MetricSample.metric_name == metric_name)
    return q.order_by(desc(MetricSample.recorded_at)).limit(limit).all()