from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_model import Project


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, project: Project) -> Project:
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get_projects_by_user(
        self, user_id: int, skip: int = 0, limit: int = 10, search: str | None = None
    ) -> list[Project]:
        query = select(Project).where(Project.user_id == user_id)
        if search:
            query = query.where(Project.name.ilike(f"%{search}%"))
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_project_by_id_and_user(
        self, project_id: int, user_id: int
    ) -> Project | None:
        query = select(Project).where(
            Project.id == project_id, Project.user_id == user_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_project(self, project: Project) -> Project:
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.commit()
