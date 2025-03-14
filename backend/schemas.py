from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class LodgingBase(BaseModel):
    name: str
    location: str
    price_per_night: float
    availability: bool
    description: str


class LodgingCreate(LodgingBase):
    pass


class LodgingResponse(BaseModel):
    id: int
    name: str
    location: str
    price_per_night: float
    availability: bool
    description: str
    created_at: datetime
    updated_at: datetime


class Config:
    from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] | None
    role: str


class UserCreate(BaseModel):
    email: str
    password: str
    role: str = Field(default="user")


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True


class LodgingUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price_per_night: Optional[float] = None
    availability: Optional[bool] = None
    description: Optional[str] = None


class BookingCreate(BaseModel):
    lodging_id: int
    start_date: date
    end_date: date
    # ...


class BookingResponse(BaseModel):
    id: int
    lodging_id: int
    user_id: int
    start_date: date
    end_date: date
