from fastapi import APIRouter, Request, HTTPException

from apps.api.v1.auth.service import router as userservice

from apps.api.v1.item.service import router as itemservice

from apps.core.security import verify_access_token


async def check_authentication(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = token.split(" ")[1]
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await call_next(request)
    return response

# itemservice.middleware("http")(check_authentication)

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(userservice, prefix="/user", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(itemservice, prefix="/items", tags=["items"])
