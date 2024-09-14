from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User, UserRepository

async def init_users(db: AsyncSession):
    pass