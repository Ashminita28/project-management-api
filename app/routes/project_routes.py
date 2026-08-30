from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database_config import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.project_schema import ProjectCreate, ProjectResponse
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskStatus
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.utils.auth_utils import get_current_user_id

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(db)
    return ProjectService(repo)


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    proj_repo = ProjectRepository(db)
    return TaskService(task_repo, proj_repo)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return await service.create_project(project, user_id)


@router.get("/", response_model=list[ProjectResponse])
async def get_my_projects(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return await service.get_user_projects(user_id, page, limit, search)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_single_project(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return await service.get_project_by_id(project_id, user_id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_single_project(
    project_id: int,
    project_update: ProjectCreate,
    user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return await service.update_project(project_id, user_id, project_update)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_project(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    await service.delete_project(project_id, user_id)


@router.post(
    "/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    project_id: int,
    task: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(project_id, task, user_id)


@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
async def get_project_tasks(
    project_id: int,
    page: int = 1,
    limit: int = 10,
    status_filter: TaskStatus | None = None,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_project_tasks(
        project_id, user_id, page, limit, status_filter
    )


@router.get("/{project_id}/summary")
async def get_project_summary(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_project_dashboard(project_id, user_id)
