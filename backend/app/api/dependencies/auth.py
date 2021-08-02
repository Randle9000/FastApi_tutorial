from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import SECRET_KEY, API_PREFIX
from app.models.user import UserInDB
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.services import auth_service
import logging

logger = logging.getLogger(__name__)

# OAuth2PasswordBearer is a class we import from FastAPI that we can instantiate by passing it the path
# that our users will send their email and password to so that they can authenticate.
# This class simply informs FastAPI that the URL provided is the one used to get a token.
# That information is used in OpenAPI and in FastAPI's interactive docs.
ouath2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/users/login/token/")


async def get_user_from_token(
         *,
        token: str = Depends(ouath2_scheme),
        user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Optional[UserInDB]:
    logger.info('dependencies - get_user_from_token')
    try:
        username = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        user = await user_repo.get_user_by_user_name(username=username)
    except Exception as e:
        raise e

    return user


def get_current_active_user(current_user: UserInDB = Depends(get_user_from_token)) -> Optional[UserInDB]:
    logger.info('dependencies - get_current_active_user')
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an active user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user
