from sqlalchemy import (
     Column, Integer, String, Enum,
     Float, Boolean, Text, DateTime,
     ForeignKey, func
)
from sqlalchemy.orm import relationship
from backend.database import Base
#  from datetime import datetime


class Lodging(Base):
    __tablename__ = "lodgings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Add relationship to Bookings
    bookings = relationship("Booking", back_populates="lodging")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum("user", "admin", name="user_roles"),
        default="user", nullable=False
    )

    # Add relationship to Bookings
    bookings = relationship("Booking", back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lodging_id = Column(Integer, ForeignKey("lodgings.id"), nullable=False)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now)
    #  updated_at = Column(DateTime, default=datetime.utcnow,
    #  onupdate=datetime.utcnow)
    # Relationship to Lodging
    lodging = relationship("Lodging", back_populates="bookings")

    # Relationship to User (if you want one)
    user = relationship("User", back_populates="bookings")
