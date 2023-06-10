from pydantic import BaseSettings
from .credentials import app_setting


class Settings(BaseSettings):
    API_V1_STR = "/api/v1"
    BACKEND_CORS_ORIGINS = [
        "http://localhost:3000", "https://localhost:8000"
    ]

    SECRET_KEY = app_setting.SECRET_KEY
    ALGORITHM = app_setting.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        case_sensitive = True


settings = Settings()
