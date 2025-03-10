from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_example():
    """Basic test to verify the test setup"""
    assert 1 + 1 == 2


def test_signup():
    """Test user signup"""
    # Log in as admin to get a token for deletion
    admin_login = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"},
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


def test_login():
    """Test user login and token retrieval"""
    response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200, "Login request failed!"
    data = response.json()
    assert "access_token" in data, "Access token missing!"
    assert data["token_type"] == "bearer", "Incorrect token type!"


def test_protected_route():
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


def test_admin_only_route_for_non_admin():
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


def test_admin_only_route_for_admin():
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


def test_read_users_me():
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


def test_read_users_me_unauthorized():
    """Ensure /users/me fails without a valid token"""
    me_response = client.get("/auth/users/me")
    assert me_response.status_code == 401
