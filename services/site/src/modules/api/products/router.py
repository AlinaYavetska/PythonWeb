from fastapi import APIRouter, Depends

from src.common.database import get_postgres
from src.modules.api.products.services import ProductService

router = APIRouter(prefix="/product")

service = ProductService()


@router.get("")
async def list_list_product(db=Depends(get_postgres)):
    return await service.get_all(db)
