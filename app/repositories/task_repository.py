from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import logger
from app.exceptions.domain import InternalError
from app.models.task_model import Task
from app.schemas.task_schema import TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: Task) -> Task:
        try:
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in create_task: {str(exc)}")
            raise InternalError("Failed to create task in database.") from exc

    def get_tasks_by_project(
        self, project_id: int, skip: int = 0, limit: int = 10, status: str | None = None
    ) -> list[Task]:
        try:
            query = self.db.query(Task).filter(Task.project_id == project_id)
            if status:
                query = query.filter(Task.status == status)
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as exc:
            logger.exception(f"Database error in get_tasks_by_project: {str(exc)}")
            raise InternalError("Failed to retrieve tasks from database.") from exc

    def get_task_by_id(self, task_id: int) -> Task | None:
        try:
            return self.db.query(Task).filter(Task.id == task_id).first()
        except SQLAlchemyError as exc:
            logger.exception(f"Database error in get_task_by_id: {str(exc)}")
            raise InternalError("Failed to retrieve task from database.") from exc

    def update_task(self, task: Task) -> Task:
        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in update_task: {str(exc)}")
            raise InternalError("Failed to update task in database.") from exc

    def delete_task(self, task: Task) -> None:
        try:
            self.db.delete(task)
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in delete_task: {str(exc)}")
            raise InternalError("Failed to delete task in database.") from exc

    def get_project_summary(self, project_id: int) -> dict:
        try:
            total = self.db.query(Task).filter(Task.project_id == project_id).count()
            todo = (
                self.db.query(Task)
                .filter(Task.project_id == project_id, Task.status == TaskStatus.TO_DO)
                .count()
            )
            in_progress = (
                self.db.query(Task)
                .filter(
                    Task.project_id == project_id, Task.status == TaskStatus.IN_PROGRESS
                )
                .count()
            )
            done = (
                self.db.query(Task)
                .filter(Task.project_id == project_id, Task.status == TaskStatus.DONE)
                .count()
            )
            return {
                "total_tasks": total,
                "todo": todo,
                "in_progress": in_progress,
                "done": done,
            }
        except SQLAlchemyError as exc:
            logger.exception(f"Database error in get_project_summary: {str(exc)}")
            raise InternalError("Failed to generate project summary.") from exc
