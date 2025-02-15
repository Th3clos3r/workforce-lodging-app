from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    role: str


class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "user"


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True
