from app.config import logger
from app.exceptions.domain import AppError, InternalError, NotFoundError
from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schema import ProjectCreate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(self, project_data: ProjectCreate, user_id: int) -> Project:
        try:
            new_project = Project(
                name=project_data.name,
                description=project_data.description,
                user_id=user_id,
            )
            created_project = self.repository.create_project(new_project)
            logger.info(
                f"User {user_id} created new project: {created_project.name} (ID: {created_project.id})"
            )
            return created_project
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in create_project: %s", e)
            raise InternalError("Failed to create project") from e

    def get_user_projects(
        self, user_id: int, page: int = 1, limit: int = 10, search: str | None = None
    ) -> list[Project]:
        try:
            skip = (page - 1) * limit
            return self.repository.get_projects_by_user(
                user_id, skip=skip, limit=limit, search=search
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in get_user_projects: %s", e)
            raise InternalError("Failed to fetch projects") from e

    def get_project_by_id(self, project_id: int, user_id: int) -> Project:
        try:
            project = self.repository.get_project_by_id_and_user(project_id, user_id)
            if not project:
                raise NotFoundError("Project not found")
            return project
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in get_project_by_id: %s", e)
            raise InternalError("Failed to fetch project") from e

    def update_project(
        self, project_id: int, user_id: int, update_data: ProjectCreate
    ) -> Project:
        try:
            project = self.get_project_by_id(project_id, user_id)
            project.name = update_data.name
            if update_data.description is not None:
                project.description = update_data.description

            updated_project = self.repository.update_project(project)
            logger.info(f"User {user_id} updated project ID: {project_id}")
            return updated_project
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in update_project: %s", e)
            raise InternalError("Failed to update project") from e

    def delete_project(self, project_id: int, user_id: int) -> None:
        try:
            project = self.get_project_by_id(project_id, user_id)
            self.repository.delete_project(project)
            logger.info(f"User {user_id} deleted project ID: {project_id}")
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in delete_project: %s", e)
            raise InternalError("Failed to delete project") from e
