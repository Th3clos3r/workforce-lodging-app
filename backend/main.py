from fastapi import FastAPI
from backend.database import engine, Base, get_db
from backend.models import User
from backend.auth import hash_password
from sqlalchemy.orm import Session
from backend.auth_routes import router as auth_router
from backend.api.routers.lodging_router import router as lodging_router
from backend.api.routers.booking_router import router as booking_router
from backend.api.routers import invoice_router

app = FastAPI()
# Create DB tables (if not already existing)
Base.metadata.create_all(bind=engine)


def seed_admin():
    db: Session = next(get_db())
    try:
        admin_email = "admin@example.com"
        admin_password = "adminpassword"
        existing = db.query(User).filter(User.email == admin_email).first()
        if not existing:
            new_admin = User(
                email=admin_email,
                hashed_password=hash_password(admin_password),
                role="admin",
            )
            db.add(new_admin)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    seed_admin()


# Include your existing routers
app.include_router(lodging_router, prefix="", tags=["Lodgings"])
app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(invoice_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Workforce Lodging API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
