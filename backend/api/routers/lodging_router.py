from fastapi import APIRouter, Depends
from backend.database import get_db
from backend.models import Lodging
from backend.schemas import LodgingResponse
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/lodgings/", response_model=List[LodgingResponse])
def get_lodgings(db: Session = Depends(get_db)):
    return db.query(Lodging).all()
