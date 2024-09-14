from fastapi import APIRouter, Depends

from src.common import database, dependencies

from src.modules.auth import service, schemas

router = APIRouter(prefix="/auth")

auth_service = service.AuthService()


@router.post(path="/customer/login")
async def login_customer(
        dto: schemas.LoginDto,
        db=Depends(database.get_postgres)):
    return await auth_service.login_customer(db, dto)


@router.post(path="/admin/login")
async def login_admin(
        dto: schemas.LoginDto,
        db=Depends(database.get_postgres)):
    return await auth_service.login_admin(db, dto)


@router.post(path="/refresh")
async def refresh_access_token(
        dto: schemas.RefreshTokenDto,
        db=Depends(database.get_postgres)):
    return await auth_service.refresh_access_token(db, dto.refresh)


@router.get(path="/admin")
async def retrieve_admin(admin=Depends(dependencies.get_admin)):
    return {"email": admin.email}


@router.get(path="/customer")
async def retrieve_customer(customer=Depends(dependencies.get_customer)):
    return {"email": customer.email}