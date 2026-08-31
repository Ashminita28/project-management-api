import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def setup_project_and_headers(client: TestClient):
    client.post(
        "/users/register",
        json={
            "name": "Task Master",
            "email": "tasks@example.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/users/login", json={"email": "tasks@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_response = client.post(
        "/projects/",
        headers=headers,
        json={"name": "Test Project", "description": "For tasks"},
    )
    project_id = proj_response.json()["id"]

    return {"headers": headers, "project_id": project_id}


def test_create_task(client: TestClient, setup_project_and_headers: dict):
    headers = setup_project_and_headers["headers"]
    project_id = setup_project_and_headers["project_id"]

    response = client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Test Task", "description": "A new task", "status": "To Do"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"


def test_get_project_dashboard(client: TestClient, setup_project_and_headers: dict):
    headers = setup_project_and_headers["headers"]
    project_id = setup_project_and_headers["project_id"]

    client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Task 1", "description": "", "status": "To Do"},
    )
    client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Task 2", "description": "", "status": "Done"},
    )

    response = client.get(f"/projects/{project_id}/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 2
    assert data["todo"] == 1
    assert data["done"] == 1


def test_get_project_tasks_filtered(
    client: TestClient, setup_project_and_headers: dict
):
    headers = setup_project_and_headers["headers"]
    project_id = setup_project_and_headers["project_id"]

    client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Task 1", "description": "", "status": "To Do"},
    )
    client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Task 2", "description": "", "status": "In Progress"},
    )

    response = client.get(
        f"/projects/{project_id}/tasks?status_filter=In%20Progress", headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Task 2"


def test_update_task(client: TestClient, setup_project_and_headers: dict):
    headers = setup_project_and_headers["headers"]
    project_id = setup_project_and_headers["project_id"]

    task_response = client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Old Task", "description": "", "status": "To Do"},
    )
    task_id = task_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={"title": "New Task", "description": "", "status": "Done"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Task"
    assert response.json()["status"] == "Done"


def test_delete_task(client: TestClient, setup_project_and_headers: dict):
    headers = setup_project_and_headers["headers"]
    project_id = setup_project_and_headers["project_id"]

    task_response = client.post(
        f"/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "To Delete", "description": "", "status": "To Do"},
    )
    task_id = task_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404
