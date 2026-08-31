from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.exceptions.domain import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise UnauthorizedError("Could not validate credentials")

        return int(user_id_str)

    except JWTError:
        raise UnauthorizedError("Could not validate credentials")
