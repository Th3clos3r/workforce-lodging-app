from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from backend.database import get_db
from backend.models import Lodging, User
from backend.schemas import LodgingResponse, LodgingCreate, LodgingUpdate
from typing import List
from backend.auth import get_current_user

router = APIRouter(prefix="/lodgings", tags=["Lodgings"])


@router.post("/", response_model=LodgingResponse)
def create_lodging(
    lodging: LodgingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Require authentication
):
    # Ensure only admins can create lodgings
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    new_lodging = Lodging(**lodging.model_dump())
    db.add(new_lodging)
    db.commit()
    db.refresh(new_lodging)
    return new_lodging


@router.get("/", response_model=List[LodgingResponse])
def get_lodgings(db: Session = Depends(get_db)):
    """Retrieve all lodgings (public access)"""
    return db.query(Lodging).all()


@router.get("/{lodging_id}", response_model=LodgingResponse)
def get_lodging(
    lodging_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a single lodging by ID (public access)"""
    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()
    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")

    return lodging


@router.put("/{lodging_id}", response_model=LodgingResponse)
def update_lodging(
    lodging_id: int,
    lodging_data: LodgingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Require authentication
):
    """Allow only admins to update a lodging"""
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()
    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")

    db.query(Lodging).filter(Lodging.id == lodging_id).update(
        {**lodging_data.dict(exclude_unset=True), "updated_at": func.now()}
    )
    db.commit()

    return db.query(Lodging).filter(Lodging.id == lodging_id).first()


@router.delete("/{lodging_id}", status_code=204)
def delete_lodging(
    lodging_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure authentication
):
    """Allow only admins to delete a lodging"""

    if not current_user:
        raise HTTPException(status_code=401,
                            detail="Could not validate credentials")

    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    lodging = db.query(Lodging).filter(Lodging.id == lodging_id).first()

    if not lodging:
        raise HTTPException(status_code=404, detail="Lodging not found")

    db.delete(lodging)
    db.commit()

    return {"message": "Lodging deleted successfully"}
