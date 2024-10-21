from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.base.repository import RepositoryBase
from src.models.borrow_item.models import BorrowItem


class BorrowRepository(RepositoryBase):
    @staticmethod
    async def get_all_by_user_id(db: AsyncSession, id: str) -> list[BorrowItem]:
        queryset = await db.execute(
            select(BorrowItem)
            .where(BorrowItem.user_id == id)
            .options(joinedload(BorrowItem.product)))
        return queryset.scalars().all()

    @staticmethod
    async def get_one(db: AsyncSession, id: int) -> BorrowItem | None:
        queryset = await db.execute(
            select(BorrowItem)
            .where(BorrowItem.id == id))
        return queryset.scalars().one_or_none()

    @staticmethod
    async def delete_by_user_id(db: AsyncSession, user_id: int):
        await db.execute(delete(BorrowItem).where(BorrowItem.user_id == user_id))
        await db.commit()



