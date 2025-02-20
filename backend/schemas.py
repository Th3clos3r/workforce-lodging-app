from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
