from fastapi import FastAPI
from backend.database import engine, Base
from backend.auth_routes import router as auth_router
from backend.api.routers.lodging_router import router as lodging_router
from backend.api.routers.booking_router import router as booking_router

app = FastAPI()

# Include your existing routers
app.include_router(lodging_router, prefix="", tags=["Lodgings"])
app.include_router(auth_router)
app.include_router(booking_router)

# Create DB tables (if not already existing)
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Workforce Lodging API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
