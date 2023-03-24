import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR = "/api/v1"

    # secrets.token_urlsafe(32)
    SECRET_KEY = "e944378eef8dc2d2187918ce509dd03fb272761e07c4b1a883c9f6b9d0fa723a"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    CLIENT_ID = "162421514963-9f6hmme9pibu77egl8ajehi25obppql3.apps.googleusercontent.com"
    PROJECT_ID = "goflow-fastapi"
    AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
    CLIENT_SECRET = "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"
    REDIRECT_URIS = [
        "http://localhost:8000/login/google/callback",
        "http://localhost:8000/login/access-token/google/callback"
    ]
    JAVASCRIPT_ORIGINS = ["http://localhost:8000", "http://localhost:5000"]

    class Config:
        case_sensitive = True


settings = Settings()
