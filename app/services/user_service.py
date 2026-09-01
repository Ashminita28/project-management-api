from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from app.config import logger, settings
from app.exceptions.domain import (
    AppError,
    ConflictError,
    InternalError,
    UnauthorizedError,
)
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def hash_password(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode("utf-8")
        hashed_password_byte_enc = hashed_password.encode("utf-8")
        return bcrypt.checkpw(
            password=password_byte_enc, hashed_password=hashed_password_byte_enc
        )

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    def register_user(self, user_data: UserCreate) -> User:
        try:
            existing_user = self.repository.get_user_by_email(user_data.email)
            if existing_user:
                raise ConflictError("Email is already registered")

            new_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=self.hash_password(user_data.password),
            )
            return self.repository.create_user(new_user)
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in register_user: %s", e)
            raise InternalError("Failed to register user") from e

    def login_user(self, email: str, password: str) -> str:
        try:
            user = self.repository.get_user_by_email(email)
            if not user or not self.verify_password(password, user.password_hash):
                raise UnauthorizedError("Invalid email or password")

            token = self.create_access_token({"sub": str(user.id)})
            return token
        except AppError:
            raise
        except Exception as e:
            logger.exception("Unexpected error in login_user: %s", e)
            raise InternalError("Login failed") from e
