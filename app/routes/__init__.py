from fastapi import APIRouter

from app.routes.dashboard_routes import router as dashboard_router
from app.routes.project_routes import router as project_router
from app.routes.task_routes import router as task_router
from app.routes.user_routes import router as user_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(project_router)
api_router.include_router(task_router)
api_router.include_router(dashboard_router)
