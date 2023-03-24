from typing import List

from fastapi import FastAPI

# from apps.api.v1.auth import router as auth_router
# from apps.core.config import settings
from apps.api.v1.read.service import router

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


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"username": user.username}
