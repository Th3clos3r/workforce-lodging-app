from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.schemas import UserCreate, UserResponse, Token, TokenData
from backend.models import User
from backend.auth import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from backend.auth import get_current_user_role
from typing import Optional


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception


@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint for user signup"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Endpoint for user login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password,
                                       user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=TokenData)
def read_users_me(current_user: TokenData = Depends(get_current_user)):
    """Returns current user information"""
    return current_user


@router.get("/protected-route")
def protected_route(token: str = Depends(oauth2_scheme)):
    """Example protected route"""
    return {"message": "You have access!", "token": token}


@router.get("/admin-only")
def admin_only(
    required_role: str = "admin",
    current_user_role: str = Depends(get_current_user_role),
):
    """Admin-only route"""
    if current_user_role != required_role:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Welcome, admin!"}


@router.delete("/delete-test-users",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_test_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin-only endpoint to delete test users"""

    if str(current_user.role) != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    db.query(User).filter(User.email.like("%testuser%")
                          ).delete(synchronize_session=False)
    db.commit()
    return {"message": "Test users deleted"}
