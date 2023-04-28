# import json
# import os
from typing import Generator

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from pydantic import ValidationError
# from sqlalchemy.orm import Session

# from apps import crud, models, schemas
# from apps.core import security
# from apps.core.config import settings
from apps.azure.session import session

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"api/login/access-token"
# )


def get_db() -> Generator:
    try:
        db = session()
        yield db
    finally:
        db.close()
