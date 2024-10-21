from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base.repository import RepositoryBase
from src.models.products.models import Product


class ProductRepository(RepositoryBase):

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Product]:
        queryset = await db.execute(select(Product).where(Product.isAvailable == True))
        return queryset.scalars().all()

    @staticmethod
    async def get_one(db: AsyncSession, id: int) -> Product | None:
        queryset = await db.execute(select(Product).where(Product.id == id))
        return queryset.scalars().one_or_none()
    
    @staticmethod
    async def update(db: AsyncSession, product: Product) -> None:
        print(product)
        stmt = (
            update(Product)
            .where(Product.id == product.id)
            .values(
                isAvailable=product.isAvailable,
                title=product.title
            )
        )
        await db.execute(stmt)
        await db.commit()
