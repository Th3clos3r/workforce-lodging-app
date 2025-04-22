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
    db: Session = next(get_db())
    try:
        admin_email = "admin@example.com"
        admin_password = "adminpassword"
        if not db.query(User).filter(User.email == admin_email).first():
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
    # Creates tables in Postgres (via engine from DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    # Then seed the admin user
    seed_admin()


# then include your routers…
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
