from uuid import UUID
from jose import jwt
from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services.auth.src.common import constants
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.src.common import database
from src.models.users import User, UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_admin(
        token=Depends(oauth2_scheme),
        db=Depends(database.get_postgres)
) -> User:
    uuid = await _verify_token(token)
    user = await _get_user(db, uuid)
    user = await _verify_admin_rights(user)
    user = await _verify_user_rights(user)
    return user


async def get_customer(
        token=Depends(oauth2_scheme),
        db=Depends(database.get_postgres)
) -> User:
    uuid = await _verify_token(token)
    user = await _get_user(db, uuid)
    user = await _verify_user_rights(user)
    return user


async def _verify_token(token: str) -> UUID:
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, constants.ALGORITHM)
        uuid = UUID(payload.get("sub"))
        if not uuid:
            raise ValueError()
        return uuid
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token has been expired."},
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid credentials."},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid token."},
        )


async def _get_user(db: AsyncSession, uuid: UUID) -> User:
    user = await UserRepository.get_one_by_uuid(db, uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid token."},
        )
    return user


async def _verify_admin_rights(user: User) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Access denied"},
        )
    return user


async def _verify_user_rights(user: User) -> User:
    if not user.is_enabled or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Access denied"},
        )
    return user