import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import backend.database as _database
import backend.auth_routes as _auth_routes
from backend.main import app
from backend.models import User
from backend.auth import hash_password

# 1) In‐memory SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# 2) Create all tables & seed the admin user
_database.Base.metadata.create_all(bind=engine)
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


# 3) Override both get_db functions so every route uses our in‑memory session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[_database.get_db] = override_get_db
app.dependency_overrides[_auth_routes.get_db] = override_get_db


# 4) Fixture for TestClient
@pytest.fixture(scope="session")
def client():
    return TestClient(app)
