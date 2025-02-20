from sqlalchemy import (
     Column, Integer, String, Enum, Float, Boolean, Text, DateTime, func
)
from backend.database import Base


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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum("user", "admin", name="user_roles"),
        default="user", nullable=False
    )
