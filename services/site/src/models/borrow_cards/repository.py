from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.base.repository import RepositoryBase
from src.models.borrow_cards.models import BorrowCard


class BorrowCardRepository(RepositoryBase):
    @staticmethod
    async def get_all_by_user_id(db: AsyncSession, id: str) -> list[BorrowCard]:
        queryset = await db.execute(
            select(BorrowCard)
            .where(BorrowCard.user_id == id)
            .options(joinedload(BorrowCard.products)))
        return queryset.scalars().unique().all()

    @staticmethod
    async def get_borrow_card_by_id(db: AsyncSession, id: int) -> BorrowCard | None:
        queryset = await db.execute(
            select(BorrowCard)
            .where(BorrowCard.id == id))
        return queryset.scalars().one_or_none()
