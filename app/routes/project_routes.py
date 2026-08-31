from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schema import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService
from app.utils.auth_utils import get_current_user_id

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(db)
    return ProjectService(repo)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(project, current_user_id)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    current_user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_user_projects(current_user_id, page, limit, search)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_project_by_id(project_id, current_user_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    return service.update_project(project_id, current_user_id, project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
):
    service.delete_project(project_id, current_user_id)
