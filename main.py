from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware

# from apps.api.v1.auth import router as auth_router
# from apps.core.config import settings
from apps.api.v1.read.service import router

# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )
app = FastAPI()
# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin)
#                        for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(router)
