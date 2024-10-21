from fastapi import APIRouter

from src.modules.api.products.router import router as product_router


router = APIRouter(prefix="/api")

router.include_router(product_router)