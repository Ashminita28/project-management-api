"""Environment configuration loader"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Load and expose environment settings for the application"""

    def __init__(self) -> None:
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEVELOPMENT")
        self.PROJECT_NAME: str = "Project Management API"
        self.PROJECT_DESCRIPTION: str = (
            "A complete backend for managing projects and tasks."
        )
        self.LOG_DIR: str = "logs"

        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "CRITICAL ERROR: SECRET_KEY environment variable is missing!"
            )
        self.JWT_SECRET_KEY: str = secret_key

        self.JWT_ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )

        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL", "sqlite:///./project_management.db"
        )


settings = Settings()
