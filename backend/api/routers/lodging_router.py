from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from backend.database import get_db
from backend.models import Lodging
from backend.schemas import LodgingResponse, LodgingCreate, LodgingUpdate
from typing import List

router = APIRouter(prefix="/lodgings")


@router.post("/", response_model=LodgingResponse)
def create_lodging(lodging: LodgingCreate, db: Session = Depends(get_db)):
    new_lodging = Lodging(**lodging.model_dump())
    db.add(new_lodging)
    db.commit()
    db.refresh(new_lodging)
    return new_lodging


@router.get("/", response_model=List[LodgingResponse])
def get_lodgings(db: Session = Depends(get_db)):
    return db.query(Lodging).all()


@router.get("/{lodging_id}", response_model=LodgingResponse)
def get_lodging(lodging_id: int, db: Session = Depends(get_db)):
    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()
    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")
    return lodging


@router.put("/{lodging_id}", response_model=LodgingResponse)
def update_lodging(lodging_id: int, lodging_data: LodgingUpdate,
                   db: Session = Depends(get_db)):
    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()
    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")

    db.query(Lodging).filter(Lodging.id == lodging_id).update(
        {**lodging_data.dict(exclude_unset=True), "updated_at": func.now()}
    )

    db.commit()

    return db.query(Lodging).filter(Lodging.id == lodging_id).first()


@router.delete("/{lodging_id}", status_code=204)
def delete_lodging(lodging_id: int, db: Session = Depends(get_db)):
    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()

    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")

    db.delete(lodging)
    db.commit()

    return {"message": "Lodging deleted successfully"}
