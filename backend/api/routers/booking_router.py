from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional

from backend.database import get_db
from backend.models import Booking, User  # Make sure Booking model is defined
from backend.schemas import BookingCreate, BookingResponse  # or BookingUpdate
from backend.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse,
             status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new booking.
    Currently requires admin role, mirroring your lodging logic.
    If you want regular users to create bookings, remove the admin check.
    """
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Optional: Check lodging existence or overlap logic if needed:
    # e.g. ensure no date overlap. For example:
    # overlap = db.query(Booking).filter(
    #     Booking.lodging_id == booking_data.lodging_id,
    #     Booking.end_date > booking_data.start_date,
    #     Booking.start_date < booking_data.end_date
    # ).first()
    # if overlap:
    #     raise HTTPException(status_code=409, detail="Date range
    # not available")

    new_booking = Booking(**booking_data.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.get("/", response_model=List[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    # Example optional filters
    user_id: Optional[int] = None,
    lodging_id: Optional[int] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    order: Optional[str] = "desc",
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    """
    Retrieve bookings with optional filters, sorting, and pagination.
    Mirrors the style from lodging_router.py.
    """
    query = db.query(Booking)

    # Apply filters if provided
    if user_id is not None:
        query = query.filter(Booking.user_id == user_id)
    if lodging_id is not None:
        query = query.filter(Booking.lodging_id == lodging_id)
    if status is not None:
        query = query.filter(Booking.status == status)

    # Apply sorting
    if sort_by in ["created_at", "start_date", "end_date"]:
        order_by_column = getattr(Booking, sort_by)
        if order == "desc":
            order_by_column = order_by_column.desc()
        query = query.order_by(order_by_column)

    # Pagination
    bookings = query.offset(offset).limit(limit).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single booking by ID (public access in this example).
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Load the existing booking
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # 2. Optional: Overlap checks or other logic
    # overlap = db.query(Booking)...
    # if overlap: raise HTTPException(status_code=409,
    # detail="Date range not available")

    # 3. Convert your Pydantic data to a dict
    #    exclude_unset=True ensures only changed fields are included
    update_data = booking_data.model_dump(exclude_unset=True)

    # If you have an updated_at column, update it:
    update_data["updated_at"] = func.now()

    # 4. Loop through update_data and set each attribute
    # on the booking instance
    for key, value in update_data.items():
        setattr(booking, key, value)

    # 5. Commit and refresh
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=204)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a booking by ID.
    Currently requires admin role to match lodging logic.
    """
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
