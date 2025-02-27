from sqlalchemy import Column, Integer, String, Enum
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum("user", "admin", name="user_roles"),
        default="user", nullable=False
    )
