from fastapi import HTTPException, status

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.auth_utils import create_access_token
from app.utils.security_utils import get_password_hash, verify_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user_data: UserCreate) -> User:
        existing_user = await self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email, name=user_data.name, password_hash=hashed_password
        )
        return await self.repository.create_user(new_user)

    async def login_user(self, user_data: UserLogin) -> dict[str, str]:
        user = await self.repository.get_user_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
