from fastapi import APIRouter, Depends

from src.common.database import get_postgres
from src.modules.customers import schemas, services

router = APIRouter(prefix="/customer")

customer_service = services.CustomerService()


@router.post(path="")
async def create_customer(dto: schemas.CreateCustomerDto, db=Depends(get_postgres)):
    return await customer_service.create(db, dto)