import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def setup_user_and_headers(client: TestClient):
    client.post(
        "/users/register",
        json={
            "name": "Project User",
            "email": "proj@example.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/users/login", json={"email": "proj@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_project_success(client: TestClient, setup_user_and_headers: dict):
    headers = setup_user_and_headers
    response = client.post(
        "/projects/",
        headers=headers,
        json={"name": "Test Project", "description": "This is a test project"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"


def test_create_project_unauthorized(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Test Project", "description": "No auth"}
    )
    assert response.status_code == 401


def test_get_user_projects(client: TestClient, setup_user_and_headers: dict):
    headers = setup_user_and_headers
    client.post("/projects/", headers=headers, json={"name": "P1", "description": "1"})
    client.post("/projects/", headers=headers, json={"name": "P2", "description": "2"})

    response = client.get("/projects/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
