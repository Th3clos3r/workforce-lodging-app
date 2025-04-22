from fastapi import FastAPI
from backend.database import engine, Base, get_db
from backend.models import User
from backend.auth import hash_password
from sqlalchemy.orm import Session

from backend.auth_routes import router as auth_router
from backend.api.routers.lodging_router import router as lodging_router
from backend.api.routers.booking_router import router as booking_router
from backend.api.routers.invoice_router import router as invoice_router

app = FastAPI()


def seed_admin() -> None:
    """
    Ensure there is an admin user in the database
    with email=admin@example.com and password=adminpassword.
    """
    db: Session = next(get_db())
    try:
        admin_email = "admin@example.com"
        admin_password = "adminpassword"

        # If no such user exists yet, create one:
        exists = db.query(User).filter(User.email == admin_email).first()
        if not exists:
            db.add(
                User(
                    email=admin_email,
                    hashed_password=hash_password(admin_password),
                    role="admin",
                )
            )
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    # 1) Create any missing tables
    Base.metadata.create_all(bind=engine)

    # 2) Seed the admin user
    seed_admin()


app.include_router(auth_router)
app.include_router(lodging_router)
app.include_router(booking_router)
app.include_router(invoice_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Workforce Lodging API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
