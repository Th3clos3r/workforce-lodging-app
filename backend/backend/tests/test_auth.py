from fastapi.testclient import TestClient
from backend.main import app  # Import your FastAPI app
import sys
import os

sys.path.append("backend")

client = TestClient(app)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_signup():
    """Test user signup"""
    response = client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "role": "user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "testuser@example.com"


def test_login():
    """Test user login and token retrieval"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    # Debugging: Print the login response
    print("Login Response JSON:", response.json())

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_route():
    """Test access to a protected route"""
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )

    # Debugging: Print the login response
    print("Protected Route - Login Response JSON:", login_response.json())
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/protected-route", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "You have access!"


def test_admin_only_route():
    """Test that non-admins cannot access admin-only route"""
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )

    # Debugging: Print the login response
    print("Admin Only Route - Login Response JSON:", login_response.json())

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/admin-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden
