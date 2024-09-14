from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common import constants, logger, seeders, database

from src.modules.customers.router import router as customer_router
from src.modules.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app):
    logger.init_logger()
    await database.create_tables_postgres()
    await seeders.run_seeders()

    yield


app = FastAPI(title="Auth Service", version="1", lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[constants.GATEWAY_HOST, constants.SITE_HOST],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(customer_router, tags=["Customer"])