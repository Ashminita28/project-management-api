from app.config import logger
from app.exceptions.domain import AppError, InternalError, NotFoundError
from app.models.task_model import Task
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskStatus


class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def _ensure_project_access(self, project_id: int, user_id: int):
        project = self.project_repo.get_project_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundError("Project not found")

    def _get_task_and_ensure_access(self, task_id: int, user_id: int) -> Task:
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        self._ensure_project_access(task.project_id, user_id)
        return task

    def create_task(self, project_id: int, task_data: TaskCreate, user_id: int) -> Task:
        try:
            self._ensure_project_access(project_id, user_id)
            new_task = Task(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                project_id=project_id,
            )
            created_task = self.task_repo.create_task(new_task)
            logger.info(
                f"User {user_id} added task '{created_task.title}' to Project {project_id}"
            )
            return created_task
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in create_task: %s", e)
            raise InternalError("Failed to create task") from e

    def get_project_tasks(
        self,
        project_id: int,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        try:
            self._ensure_project_access(project_id, user_id)
            skip = (page - 1) * limit
            return self.task_repo.get_tasks_by_project(
                project_id, skip=skip, limit=limit, status=status
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in get_project_tasks: %s", e)
            raise InternalError("Failed to fetch tasks") from e

    def get_single_task(self, task_id: int, user_id: int) -> Task:
        try:
            return self._get_task_and_ensure_access(task_id, user_id)
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in get_single_task: %s", e)
            raise InternalError("Failed to fetch task") from e

    def update_task(self, task_id: int, user_id: int, update_data: TaskCreate) -> Task:
        try:
            task = self._get_task_and_ensure_access(task_id, user_id)
            task.title = update_data.title
            if update_data.description is not None:
                task.description = update_data.description
            task.status = update_data.status

            updated_task = self.task_repo.update_task(task)
            logger.info(
                f"User {user_id} updated task ID: {task_id} to status '{task.status}'"
            )
            return updated_task
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in update_task: %s", e)
            raise InternalError("Failed to update task") from e

    def delete_task(self, task_id: int, user_id: int) -> None:
        try:
            task = self._get_task_and_ensure_access(task_id, user_id)
            self.task_repo.delete_task(task)
            logger.info(f"User {user_id} deleted task ID: {task_id}")
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in delete_task: %s", e)
            raise InternalError("Failed to delete task") from e

    def get_project_dashboard(self, project_id: int, user_id: int) -> dict:
        try:
            self._ensure_project_access(project_id, user_id)
            return self.task_repo.get_project_summary(project_id)
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in get_project_dashboard: %s", e)
            raise InternalError("Failed to fetch dashboard") from e
