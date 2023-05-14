from pydantic import BaseSettings
from .credentials import app_setting, google_setting


class Settings(BaseSettings):
    API_V1_STR = "/api/v1"
    BACKEND_CORS_ORIGINS = [
        "http://localhost:3000",
    ]

    SECRET_KEY = app_setting.SECRET_KEY  # secrets.token_urlsafe(32)
    ALGORITHM = app_setting.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CLIENT_ID = google_setting.CLIENT_ID
    # PROJECT_ID = "goflow-fastapi"
    # AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    # TOKEN_URI = "https://oauth2.googleapis.com/token"
    # AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
    # CLIENT_SECRET = google_setting.CLIENT_SECRET
    # REDIRECT_URIS = [
    #     "https://localhost:8000/user/login/access-token/google/callback"
    # ]
    # JAVASCRIPT_ORIGINS = ["https://localhost:8000"]

    class Config:
        case_sensitive = True


settings = Settings()
