import logging

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models.users import User, UserRepository
from src.modules.customers import schemas

logger = logging.getLogger(__name__)


class CustomerService:
    async def create(self, db: AsyncSession, dto: schemas.CreateCustomerDto):
        try:
            customer = await UserRepository.create(db, User(**dto.model_dump()))
            return JSONResponse(content=schemas.CustomerDetailDto(**customer.__dict__).model_dump(), status_code=201)

        except IntegrityError as e:
            raise HTTPException(detail="Email already taken", status_code=400)