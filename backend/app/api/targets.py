from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.target import Target
from app.schemas.target import TargetCreate, TargetOut
 
router = APIRouter(prefix="/targets", tags=["targets"])
 
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
