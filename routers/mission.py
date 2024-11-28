from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.mission import Mission
from models.spy_cat import SpyCat
from schemas.mission import MissionCreate
from services import mission as MissionService

mission = APIRouter()


@mission.post("/", response_model=MissionCreate, tags=["mission"])
def create(mission: MissionCreate, db: Session = Depends(get_db)):
    if mission.spy_cat_id != 0:
        db_spy_cat = db.query(SpyCat).filter(SpyCat.id == mission.spy_cat_id).first()
        if not db_spy_cat:
            raise HTTPException(status_code=404, detail="Cat not found")

    target_names = set()
    for target in mission.targets:
        if (target.name, target.country, target.notes) in target_names:
            raise HTTPException(status_code=400, detail=f"Duplicate target: {target.name} in country {target.country}")
        target_names.add((target.name, target.country, target.notes))

    return MissionService.create_mission(db, mission)


@mission.get("/{mission_id}", response_model=MissionCreate, tags=["mission"])
def get(mission_id: int = None, db: Session = Depends(get_db)):
    db_mission = MissionService.get_mission(db, mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission


@mission.get("/", response_model=List[MissionCreate], tags=["mission"])
def list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    return MissionService.list_missions(db, skip, limit)


@mission.put("/{mission_id}/assign-cat/{spy_cat_id}", response_model=MissionCreate, tags=["mission"])
def assign_cat(mission_id: int = None, spy_cat_id: int = None, db: Session = Depends(get_db)):
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if spy_cat_id != 0:
        db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
        if not db_spy_cat:
            raise HTTPException(status_code=404, detail="Cat not found")

        if db_mission.spy_cat_id:
            raise HTTPException(status_code=400,
                                detail=f"Mission already assigned to a cat with ID {db_mission.spy_cat_id}")

    return MissionService.assign_cat_to_mission(db, mission_id, spy_cat_id)


@mission.delete("/{mission_id}", tags=["mission"])
def delete(mission_id: int = None, db: Session = Depends(get_db)):
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.spy_cat_id != 0:
        if db_mission.spy_cat_id:
            raise HTTPException(status_code=400, detail="Cannot delete a mission assigned to a cat")

    return MissionService.delete_mission(db, mission_id)
