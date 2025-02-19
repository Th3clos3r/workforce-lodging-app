from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


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
