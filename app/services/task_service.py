from fastapi import HTTPException

from app.models.task_model import Task
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskStatus


class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    async def _ensure_project_access(self, project_id: int, user_id: int):
        project = await self.project_repo.get_project_by_id_and_user(
            project_id, user_id
        )
        if not project:
            raise HTTPException(
                status_code=404, detail="Project not found or unauthorized"
            )

    async def _get_task_and_ensure_access(self, task_id: int, user_id: int) -> Task:
        task = await self.task_repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await self._ensure_project_access(task.project_id, user_id)
        return task

    async def create_task(
        self, project_id: int, task_data: TaskCreate, user_id: int
    ) -> Task:
        await self._ensure_project_access(project_id, user_id)
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            project_id=project_id,
        )
        return await self.task_repo.create_task(new_task)

    async def get_project_tasks(
        self,
        project_id: int,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        await self._ensure_project_access(project_id, user_id)
        skip = (page - 1) * limit
        return await self.task_repo.get_tasks_by_project(
            project_id, skip=skip, limit=limit, status=status
        )

    async def get_single_task(self, task_id: int, user_id: int) -> Task:
        return await self._get_task_and_ensure_access(task_id, user_id)

    async def update_task(
        self, task_id: int, user_id: int, update_data: TaskCreate
    ) -> Task:
        task = await self._get_task_and_ensure_access(task_id, user_id)
        task.title = update_data.title
        if update_data.description is not None:
            task.description = update_data.description
        task.status = update_data.status
        return await self.task_repo.update_task(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self._get_task_and_ensure_access(task_id, user_id)
        await self.task_repo.delete_task(task)

    async def get_project_dashboard(self, project_id: int, user_id: int) -> dict:
        await self._ensure_project_access(project_id, user_id)
        return await self.task_repo.get_project_summary(project_id)
