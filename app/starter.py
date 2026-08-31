from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import logger, settings
from app.exceptions.domain import AppError
from app.exceptions.handlers import (
    app_error_handler,
    global_exception_handler,
    http_exception_handler,
    request_validation_handler,
)
from app.routes import api_router


class AppStarter:
    def __init__(self) -> None:
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_DESCRIPTION,
            version="1.0.0",
        )

    def _configure_exception_handlers(self) -> None:
        self.app.add_exception_handler(AppError, app_error_handler)
        self.app.add_exception_handler(Exception, global_exception_handler)
        self.app.add_exception_handler(
            RequestValidationError, request_validation_handler
        )
        self.app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    def _configure_routes(self) -> None:
        self.app.include_router(api_router)

    def _initialize_database(self) -> None:
        from app.config.database_config import Base, engine

        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized.")

    def create_app(self) -> FastAPI:
        self._initialize_database()
        self._configure_exception_handlers()
        self._configure_routes()
        logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode.")
        return self.app
