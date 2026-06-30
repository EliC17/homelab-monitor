from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.metric import MetricSample
from app.schemas.metric import MetricIngest
 
router = APIRouter(tags=["metrics"])
 
@router.post("/metrics/ingest", status_code=201)
def ingest(payload: list[MetricIngest], db: Session = Depends(get_db)):
    rows = [MetricSample(**m.model_dump()) for m in payload]
    db.bulk_save_objects(rows)
    db.commit()
    return {"ingested": len(rows)}
