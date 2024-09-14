from uuid import UUID
from datetime import datetime, timedelta, UTC

from jose import jwt
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import constants, dependencies
from src.modules.auth import schemas
from src.models.users import User, UserRepository


class AuthService:

    async def login_customer(self, db: AsyncSession, dto: schemas.LoginDto):
        user = await self._get_user_by_email(db, dto.email)
        if not user.is_enabled:
            raise HTTPException(detail="Access denied", status_code=403)
        if not self._verify_password(dto.password, user.password):
            raise HTTPException(detail="Incorrect password", status_code=401)
        return JSONResponse(
            content={
                "access": self._create_access_token(user.uuid),
                "refresh": self._create_refresh_token(user.uuid)
            },
            status_code=200
        )

    async def login_admin(self, db: AsyncSession, dto: schemas.LoginDto):
        user = await self._get_user_by_email(db, dto.email)
        if not user.is_enabled or not user.is_admin:
            raise HTTPException(detail="Access denied", status_code=403)
        if not self._verify_password(dto.password, user.password):
            raise HTTPException(detail="Incorrect password", status_code=401)
        return JSONResponse(
            content={
                "access": self._create_access_token(user.uuid),
                "refresh": self._create_refresh_token(user.uuid)
            },
            status_code=200
        )

    async def refresh_access_token(self, db: AsyncSession, token: str):
        uuid = await dependencies._verify_token(token)
        if not uuid:
            raise HTTPException("Invalid token", status_code=400)
        user = await self._get_user_by_uuid(db, uuid)
        return JSONResponse(
            content={
                "access": self._create_access_token(user.uuid)
            },
            status_code=200
        )

    async def _get_user_by_email(self, db: AsyncSession, email: str) -> User:
        user = await UserRepository.get_one_by_email(db, email)
        if not user:
            raise HTTPException(detail="User was not found", status_code=404)
        return user

    async def _get_user_by_uuid(self, db: AsyncSession, uuid: UUID) -> User:
        user = await UserRepository.get_one_by_uuid(db, uuid)
        if not user:
            raise HTTPException(detail="User was not found", status_code=404)
        return user

    def _verify_password(self, password: str, hashed_pass: str) -> bool:
        return password == hashed_pass

    def _create_access_token(self, sub: any) -> str:
        return self.__generate_jwt_token(sub, datetime.now() + timedelta(
            minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES
        ))

    def _create_refresh_token(self, sub: any) -> str:
        return self.__generate_jwt_token(sub, datetime.now() + timedelta(
            minutes=constants.REFRESH_TOKEN_EXPIRE_MINUTES
        ))

    def __generate_jwt_token(self, sub: any, expires_delta: datetime) -> str:
        return jwt.encode(
            claims={
                "exp": expires_delta,
                "sub": str(sub)},
            key=constants.SECRET_KEY,
            algorithm=constants.ALGORITHM
        )