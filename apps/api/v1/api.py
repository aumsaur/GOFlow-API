from fastapi import APIRouter, Request, HTTPException

from apps.api.v1.user.service import router as user_service
from apps.api.v1.item.service import router as item_service
from apps.core.security import verify_access_token, decode_access_token

import json


async def authenticate_token(request: Request, call_next):
    """
    Middleware function to authenticate access tokens.

    Parameters:
    - request (Request): The incoming request.
    - call_next (Callable): The next function in the middleware chain.

    Returns:
    - Any: The response from the next function.

    Raises:
    - HTTPException: If the request is not authorized.
    """
    public_paths = ["/", "/favicon.ico", "/openapi.json", "/docs", "/user/login/access-token", "/user/register",
                    "/user/login-google/access-token", "/user/me/reset-password"]

    if request.url.path not in public_paths:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split("Bearer ")[1]
            request.state.user_id = json.loads(
                decode_access_token(token).get("sub"))
            request.state.token_exp = verify_access_token(token)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    response = await call_next(request)
    return response

api_router = APIRouter()

api_router.include_router(user_service, prefix="/user", tags=["Users"])

api_router.include_router(item_service, prefix="/item", tags=["Items"])
