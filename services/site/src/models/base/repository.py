from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase[T]:
    @staticmethod
    async def flush(db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.flush([obj])
        return obj

    @staticmethod
    async def create[T](db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def get_one[T](*args, **kwargs) -> T:
        raise NotImplemented()

    @staticmethod
    async def get_all[T](*args, **kwargs) -> list[T]:
        raise NotImplemented()

    @staticmethod
    async def update[T](db: AsyncSession, obj: T) -> T:
        await db.commit()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def delete[T](db: AsyncSession, obj: T) -> None:
        await db.delete(obj)
        await db.commit()
