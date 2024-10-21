from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products.repository import ProductRepository


class ProductService:

    async def get_all(self, db: AsyncSession):
        products = await ProductRepository.get_all(db)
        return JSONResponse(content=jsonable_encoder(products), status_code=200)
