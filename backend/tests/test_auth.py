import os
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import backend.database as _database
import backend.auth_routes as _auth_routes
from backend.main import app
from backend.models import User
from backend.auth import hash_password
# Use environment variable if available (for GitHub Actions),
# otherwise use SQLite
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///:memory:"
)

# Initialize engine based on database type
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # For PostgreSQL in GitHub Actions
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


def test_example():
    assert 1 + 1 == 2


def test_signup(client):
    """Test user signup"""
    # Log in as admin to get a token for deletion
    admin_login = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    admin_token = admin_login.json().get("access_token")
    assert admin_token, "No admin token returned!"

    headers = {"Authorization": f"Bearer {admin_token}"}

    # Ensure cleanup using the admin token
    delete_response = client.delete("/auth/delete-test-users", headers=headers)
    assert delete_response.status_code == 204, "Failed to clean up test users!"

    # Proceed with signup after cleanup
    response = client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "role": "user",
        },
    )

    assert response.status_code == 200, f"Signup failed: {response.json()}"


# Create session maker
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Create all tables & seed the admin user
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


# Override both get_db functions so every route uses our in‑memory session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[_database.get_db] = override_get_db
app.dependency_overrides[_auth_routes.get_db] = override_get_db


# Fixture for TestClient
@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_login(client):
    """Test user login and token retrieval"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200, "Login request failed!"
    data = response.json()
    assert "access_token" in data, "Access token missing!"
    assert data["token_type"] == "bearer", "Incorrect token type!"


def test_protected_route(client):
    """Test access to a protected route"""
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )

    token = login_response.json()["access_token"]
    assert token, "No token returned from login!"

    response = client.get(
        "/auth/protected-route", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "You have access!"


def test_admin_only_route_for_non_admin(client):
    """Test that non-admins cannot access admin-only route"""

    login_response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )

    token = login_response.json().get("access_token")
    assert token, "No access token returned!"

    response = client.get(
        "/auth/admin-only",
        params={"required_role": "admin"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403, (
        "Non-admin should not access admin route!"
    )


def test_admin_only_route_for_admin(client):
    """Test that admins can access admin-only route"""
    # Log in as admin
    login_response = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"},
    )
    token = login_response.json().get("access_token")
    assert token, "No access token returned!"

    response = client.get(
        "/auth/admin-only",
        params={"required_role": "admin"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, (
        "Admin should be able to access this route!"
    )
    assert response.json().get("message") == "Welcome, admin!"


def test_read_users_me(client):
    """Test the /users/me endpoint"""

    login_response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me_response = client.get("/auth/users/me", headers=headers)
    assert me_response.status_code == 200
    data = me_response.json()
    assert data.get("sub") == "testuser@example.com", (
        "Incorrect user returned!"
    )


def test_read_users_me_unauthorized(client):
    """Ensure /users/me fails without a valid token"""
    me_response = client.get("/auth/users/me")
    assert me_response.status_code == 401
