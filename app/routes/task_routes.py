from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database_config import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskResponse
from app.services.task_service import TaskService
from app.utils.auth_utils import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    proj_repo = ProjectRepository(db)
    return TaskService(task_repo, proj_repo)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_single_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_single_task(task_id, user_id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_single_task(
    task_id: int,
    task_update: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return await service.update_task(task_id, user_id, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    await service.delete_task(task_id, user_id)
