from fastapi.testclient import TestClient


def test_register_user_success(client: TestClient):
    response = client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "dup@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/users/register",
        json={
            "name": "Test User 2",
            "email": "dup@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "conflict"


def test_login_user_success(client: TestClient):
    client.post(
        "/users/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/users/login", json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
