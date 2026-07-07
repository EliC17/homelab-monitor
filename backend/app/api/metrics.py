from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.metric import MetricSample
from app.models.alert import AlertRule
from app.schemas.metric import MetricIngest
from app.services.evaluator import evaluate_rule

router = APIRouter(tags=["metrics"])

@router.post("/metrics/ingest", status_code=201)
def ingest(payload: list[MetricIngest], db: Session = Depends(get_db)):
    rows = [MetricSample(**m.model_dump()) for m in payload]
    db.bulk_save_objects(rows)
    db.commit()

    # evaluate alert rules against each newly ingested sample
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