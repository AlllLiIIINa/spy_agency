from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.target import Target
from schemas.target import TargetCreate, TargetUpdate
from services import mission as MissionService

target = APIRouter()


@target.put("/{target_id}", response_model=TargetCreate, tags=["target"])
def update_notes(target_id: int = None, data: TargetUpdate = None, db: Session = Depends(get_db)):
    db_target = db.query(Target).filter(Target.id == target_id).first()

    if not db_target:
        raise HTTPException(status_code=404, detail="Target not found")

    if db_target.complete:
        raise HTTPException(status_code=400, detail="Cannot update a completed target")

    return MissionService.update_target(db, target_id, data.notes, data.complete)
