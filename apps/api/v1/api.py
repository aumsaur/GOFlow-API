import json
from fastapi import APIRouter, Request, HTTPException

from apps.api.v1.user.service import router as user_service

from apps.api.v1.item.service import router as item_service

from apps.core.security import verify_access_token, decode_access_token


async def authenticate_token(request: Request, call_next):
    protected_paths = ["/item/read", "/item/update", "/item/create",
                       "/item/fetch", "/item/delete", "/user/me",
                       "/user/me/update", "/user/me/change-password",
                       "/user/delete"]
    print(request.url.path)
    if any(request.url.path.startswith(prefix) for prefix in protected_paths):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            request.state.token_sub = json.loads(
                decode_access_token(token).get("sub", "{}"))
            request.state.token_exp = verify_access_token(token)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    response = await call_next(request)
    return response

api_router = APIRouter()

api_router.include_router(user_service, prefix="/user", tags=["Users"])

api_router.include_router(item_service, prefix="/item", tags=["Items"])
