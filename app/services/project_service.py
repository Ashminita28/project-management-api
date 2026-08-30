from fastapi import HTTPException

from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schema import ProjectCreate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self, project_data: ProjectCreate, user_id: int
    ) -> Project:
        new_project = Project(
            name=project_data.name,
            description=project_data.description,
            user_id=user_id,
        )
        return await self.repository.create_project(new_project)

    async def get_user_projects(
        self, user_id: int, page: int = 1, limit: int = 10, search: str | None = None
    ) -> list[Project]:
        skip = (page - 1) * limit
        return await self.repository.get_projects_by_user(
            user_id, skip=skip, limit=limit, search=search
        )

    async def get_project_by_id(self, project_id: int, user_id: int) -> Project:
        project = await self.repository.get_project_by_id_and_user(project_id, user_id)
        if not project:
            raise HTTPException(
                status_code=404, detail="Project not found or unauthorized"
            )
        return project

    async def update_project(
        self, project_id: int, user_id: int, update_data: ProjectCreate
    ) -> Project:
        project = await self.get_project_by_id(project_id, user_id)
        project.name = update_data.name
        if update_data.description is not None:
            project.description = update_data.description
        return await self.repository.update_project(project)

    async def delete_project(self, project_id: int, user_id: int) -> None:
        project = await self.get_project_by_id(project_id, user_id)
        await self.repository.delete_project(project)
