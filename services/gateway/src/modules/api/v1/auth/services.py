import json
import httpx
from fastapi import Request

from src.common import constants


class ProxyAuthService:
    auth_service_host = f"http://{constants.AUTH_SERVICE_HOST}:{constants.AUTH_SERVICE_PORT}"
    async def proxy_request(self, proxy_path: str, request: Request):
        service_url = f"{self.auth_service_host}/auth/{proxy_path}"
        headers = dict(request.headers)
        print(json.loads(await request.body()) )
        print(headers)

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=service_url,
                # headers=headers,
                params=request.query_params,
                json=json.loads(await request.body()) if request.method in ("POST", "PUT") else None,
            )
            return response.json()