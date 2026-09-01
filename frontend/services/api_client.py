import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")

""" user managements API's"""


def login_user(email: str, password: str):
    response = requests.post(
        f"{BASE_API_URL}/users/login",
        json={"email": email, "password": password},
    )
    return response


def register_user(name: str, email: str, password: str):
    response = requests.post(
        f"{BASE_API_URL}/users/register",
        json={"name": name, "email": email, "password": password},
    )
    return response


""" project managements API's"""


def get_projects(token: str, page: int = 1, limit: int = 10, search: str = ""):
    headers = {"Authorization": f"Bearer {token}"}

    params: dict = {
        "page": page,
        "limit": limit,
    }
    if search:
        params["search"] = search

    response = requests.get(f"{BASE_API_URL}/projects", headers=headers, params=params)
    return response


def create_project(token: str, name: str, description: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_API_URL}/projects/",
        headers=headers,
        json={"name": name, "description": description},
    )
    return response


def get_project(token: str, project_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_API_URL}/projects/{project_id}", headers=headers)
    return response


def update_project(token: str, project_id: int, name: str, description: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BASE_API_URL}/projects/{project_id}",
        headers=headers,
        json={"name": name, "description": description},
    )
    return response


def delete_project(token: str, project_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_API_URL}/projects/{project_id}", headers=headers)
    return response


""" Task managements API's"""


def create_task(
    token: str,
    project_id: int,
    title: str,
    description: str,
    status: str,
):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_API_URL}/projects/{project_id}/tasks",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "status": status,
        },
    )

    return response


def get_project_tasks(
    token: str,
    project_id: int,
    page: int = 1,
    limit: int = 10,
    status_filter: str | None = None,
):
    headers = {"Authorization": f"Bearer {token}"}

    params: dict = {
        "page": page,
        "limit": limit,
    }

    if status_filter:
        params["status_filter"] = status_filter

    response = requests.get(
        f"{BASE_API_URL}/projects/{project_id}/tasks",
        headers=headers,
        params=params,
    )

    return response


def get_task(
    token: str,
    task_id: int,
):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{BASE_API_URL}/tasks/{task_id}",
        headers=headers,
    )

    return response


def update_task(
    token: str,
    task_id: int,
    title: str,
    description: str,
    status: str,
):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(
        f"{BASE_API_URL}/tasks/{task_id}",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "status": status,
        },
    )

    return response


def delete_task(
    token: str,
    task_id: int,
):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(
        f"{BASE_API_URL}/tasks/{task_id}",
        headers=headers,
    )

    return response


""" Dashboard stats API"""


def get_project_summary(
    token: str,
    project_id: int,
):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{BASE_API_URL}/projects/{project_id}/summary",
        headers=headers,
    )

    return response
