
from fastapi import FastAPI

from src.modules.api.v1.router import router as api_v1_router


app = FastAPI(
    title="API Gateway",
    version="1"
)
app.include_router(api_v1_router) 