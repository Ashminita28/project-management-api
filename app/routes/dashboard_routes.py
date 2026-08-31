from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.utils.auth_utils import get_current_user_id

router = APIRouter(tags=["Dashboard"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


@router.get("/projects/{project_id}/summary")
def get_project_dashboard(
    project_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: TaskService = Depends(get_task_service),
):
    return service.get_project_dashboard(project_id, current_user_id)
