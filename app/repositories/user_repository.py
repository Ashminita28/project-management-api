from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import logger
from app.exceptions.domain import InternalError
from app.models.user_model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as exc:
            logger.exception(f"Database error in get_user_by_email: {str(exc)}")
            raise InternalError("Failed to retrieve user from database.") from exc

    def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception(f"Database error in create_user: {str(exc)}")
            raise InternalError("Failed to create user in database.") from exc
