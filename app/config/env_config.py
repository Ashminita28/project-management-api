"""Environment configuration loader"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Load and expose environment settings for the application"""

    def __init__(self) -> None:
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEVELOPMENT")
        self.PROJECT_NAME: str = "Project Management API"
        self.JWT_SECRET_KEY: str = os.getenv(
            "SECRET_KEY", "super-secret-key-for-local-dev-only"
        )
        self.JWT_ALGORITHM: str = "HS256"
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        self.LOG_DIR: str = "logs"
        self.PROJECT_DESCRIPTION: str = (
            "A complete backend for managing projects and tasks."
        )
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL", "sqlite:///./project_management.db"
        )


settings = Settings()
