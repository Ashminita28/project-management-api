from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskStatus
from app.services.task_service import TaskService
from app.utils.auth_utils import get_current_user_id

router = APIRouter(tags=["Tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    task: TaskCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(project_id, task, current_user_id)


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
def get_project_tasks(
    project_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status_filter: TaskStatus | None = Query(None, alias="status_filter"),
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.get_project_tasks(
        project_id, current_user_id, page, limit, status_filter
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.get_single_task(task_id, current_user_id)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.update_task(task_id, current_user_id, task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    service.delete_task(task_id, current_user_id)
