from fastapi import APIRouter, Request

from src.modules.api.v1.auth import services


router = APIRouter(prefix="/auth", tags=["Authorization"])

auth_proxy = services.ProxyAuthService()

@router.api_route("/{proxy_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_service_proxy(proxy_path: str, request: Request):
    return await auth_proxy.proxy_request(proxy_path, request)