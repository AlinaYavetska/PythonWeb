from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.common.database import create_tables_postgres
from src.modules.mvc.router import router as mvc_router
from src.modules.api.router import router as api_router


@asynccontextmanager
async def lifespan(app):
    await create_tables_postgres()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(mvc_router)
app.include_router(api_router)
