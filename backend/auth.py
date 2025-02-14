from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user_role(required_role: str):
    def role_checker(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str | None = payload.get("sub")
            if email is None:
                raise credentials_exception

            user = db.query(User).filter(User.email == email).first()
            if user is None:
                raise credentials_exception

            print(f"User found: {user.email}, Role: {user.role}")

            if str(user.role) != required_role:
                raise HTTPException(status_code=403,
                                    detail="Not enough permissions")

            return user
        except JWTError:
            raise credentials_exception

    return role_checker


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
