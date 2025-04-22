import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.database import Base, get_db
from backend.main import app
from backend.models import User
from backend.auth import hash_password

# 1) In‑memory SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# 2) Create tables & seed admin
Base.metadata.create_all(bind=engine)
db = TestingSessionLocal()
db.add(
    User(
        email="admin@example.com",
        hashed_password=hash_password("adminpassword"),
        role="admin",
    )
)
db.commit()
db.close()


# 3) Override get_db for all routes/tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# 4) Make a TestClient fixture
@pytest.fixture(scope="session")
def client():
    return TestClient(app)
