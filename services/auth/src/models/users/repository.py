from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users.models import User
from src.models.base import RepositoryBase


class UserRepository(RepositoryBase):
    @staticmethod
    async def get_one_by_uuid(db: AsyncSession, uuid: UUID) -> User | None:
        queryset = await db.execute(
            select(User)
            .where(User.uuid == uuid)
        )
        return queryset.scalars().one_or_none()

    @staticmethod
    async def get_one_by_email(db: AsyncSession, email: str) -> User | None:
        queryset = await db.execute(
            select(User)
            .where(User.email == email)
        )
        return queryset.scalars().one_or_none()

    @staticmethod
    async def get_one_by_email_is_admin(db: AsyncSession, email: str) -> User | None:
        queryset = await db.execute(
            select(User)
            .where(
                User.email == email,
                User.is_admin == True)
        )
        return queryset.scalars().one_or_none()