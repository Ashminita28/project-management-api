from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_model import Task
from app.schemas.task_schema import TaskStatus


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: Task) -> Task:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_tasks_by_project(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 10,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        query = select(Task).where(Task.project_id == project_id)
        if status:
            query = query.where(Task.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_task_by_id(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_task(self, task: Task) -> Task:
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()

    async def get_project_summary(self, project_id: int) -> dict:
        query = (
            select(Task.status, func.count(Task.id))
            .where(Task.project_id == project_id)
            .group_by(Task.status)
        )
        result = await self.db.execute(query)

        summary = {"total_tasks": 0, "todo": 0, "in_progress": 0, "done": 0}
        for status_val, count in result.all():
            summary["total_tasks"] += count
            if status_val == TaskStatus.TO_DO:
                summary["todo"] = count
            elif status_val == TaskStatus.IN_PROGRESS:
                summary["in_progress"] = count
            elif status_val == TaskStatus.DONE:
                summary["done"] = count
        return summary
