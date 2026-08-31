from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import logger
from app.exceptions.domain import InternalError
from app.models.project_model import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project: Project) -> Project:
        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in create_project: {str(exc)}")
            raise InternalError("Failed to create project in database.") from exc

    def get_projects_by_user(
        self, user_id: int, skip: int = 0, limit: int = 10, search: str | None = None
    ) -> list[Project]:
        try:
            query = self.db.query(Project).filter(Project.user_id == user_id)
            if search:
                query = query.filter(Project.name.contains(search))
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as exc:
            logger.exception(f"Database error in get_projects_by_user: {str(exc)}")
            raise InternalError("Failed to retrieve projects from database.") from exc

    def get_project_by_id_and_user(
        self, project_id: int, user_id: int
    ) -> Project | None:
        try:
            return (
                self.db.query(Project)
                .filter(Project.id == project_id, Project.user_id == user_id)
                .first()
            )
        except SQLAlchemyError as exc:
            logger.exception(
                f"Database error in get_project_by_id_and_user: {str(exc)}"
            )
            raise InternalError("Failed to retrieve project from database.") from exc

    def update_project(self, project: Project) -> Project:
        try:
            self.db.commit()
            self.db.refresh(project)
            return project
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in update_project: {str(exc)}")
            raise InternalError("Failed to update project in database.") from exc

    def delete_project(self, project: Project) -> None:
        try:
            self.db.delete(project)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in delete_project: {str(exc)}")
            raise InternalError("Failed to delete project in database.") from exc
