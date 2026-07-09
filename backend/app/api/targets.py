from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.target import Target
from app.schemas.target import TargetCreate, TargetOut
import os
import httpx
 
router = APIRouter(prefix="/targets", tags=["targets"])
COLLECTOR_SECRET = os.environ.get("COLLECTOR_SECRET", "")
 
@router.get("", response_model=list[TargetOut])
def list_targets(db: Session = Depends(get_db)):
    return db.query(Target).all()
 
@router.post("", response_model=TargetOut, status_code=201)
def create_target(payload: TargetCreate, db: Session = Depends(get_db)):
    target = Target(**payload.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target
 
@router.get("/{target_id}", response_model=TargetOut)
def get_target(target_id: str, db: Session = Depends(get_db)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(404, "Target not found")
    return target

@router.patch("/{target_id}", response_model=TargetOut)
def update_target(target_id: str, payload: dict, db: Session = Depends(get_db)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(404, "Target not found")
    for key, value in payload.items():
        setattr(target, key, value)
    db.commit()
    db.refresh(target)
    return target

@router.post("/{target_id}/poll", status_code=202)
async def trigger_poll(target_id: str, db: Session = Depends(get_db)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(404, "Target not found")
    collector_url = os.environ.get("COLLECTOR_INTERNAL_URL", "http://collector:9000")
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{collector_url}/poll/{target_id}",
                headers={"x-collector-secret": COLLECTOR_SECRET},
                timeout=10.0
            )
    except Exception as e:
        raise HTTPException(503, f"Collector unreachable: {e}")
    return {"status": "poll triggered"}