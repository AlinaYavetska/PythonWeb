from src.common.database import SessionLocal
from src.common.seeders.users import init_users


async def run_seeders():
    async with SessionLocal() as db:
        await init_users(db)