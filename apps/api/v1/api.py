from fastapi import APIRouter

from apps.api.v1.auth.service import router as userservice

from apps.api.v1.item.service import router as itemservice

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(userservice, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(itemservice, prefix="/items", tags=["items"])
