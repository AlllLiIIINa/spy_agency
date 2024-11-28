from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.spy_cat import SpyCat
from schemas.spy_cat import SpyCatCreate, SpyCatUpdate
from services import spy_cat as SpyCatService

spy_cat = APIRouter()


@spy_cat.post("/", response_model=SpyCatCreate, tags=["spy_cat"])
def create(spy_cat: SpyCatCreate, db: Session = Depends(get_db)):
    is_valid_breed = SpyCatService.validate_breed(spy_cat.breed)
    if not is_valid_breed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid breed '{spy_cat.breed}'. Please provide a valid breed from TheCatAPI."
        )
    return SpyCatService.create_cat(db, spy_cat)


@spy_cat.get("/{spy_cat_id}", response_model=SpyCatCreate, tags=["spy_cat"])
def get(spy_cat_id: int = None, db: Session = Depends(get_db)):
    cats = SpyCatService.get_spy_cat(db, spy_cat_id)
    if cats is None:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return cats


@spy_cat.get("/", response_model=List[SpyCatCreate], tags=["spy_cat"])
def list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    return SpyCatService.list_spy_cats(db, skip, limit)


@spy_cat.put("/{spy_cat_id}", response_model=SpyCatUpdate, tags=["spy_cat"])
def update_salary(spy_cat_id: int = None, data: SpyCatUpdate = None, db: Session = Depends(get_db)):
    db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    if not db_spy_cat:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return SpyCatService.update_spy_cat_salary(db, spy_cat_id, data.salary)


@spy_cat.delete("/{spy_cat_id}", tags=["spy_cat"])
def delete(spy_cat_id: int = None, db: Session = Depends(get_db)):
    db_spy_cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    if not db_spy_cat:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return SpyCatService.delete_spy_cat(db, spy_cat_id)
