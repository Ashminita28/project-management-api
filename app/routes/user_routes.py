from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.register_user(user)


@router.post("/login")
def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    token = service.login_user(user.email, user.password)
    return {"access_token": token, "token_type": "bearer"}
