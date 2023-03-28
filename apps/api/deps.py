import json
import os
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.core import security
# from apps.core.config import settings
from apps.azure.session import session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/login/access-token"
)


def get_db() -> Generator:
    try:
        db = session()
        yield db
    finally:
        db.close()


# def get_db() -> Generator:
    # USERS_FILE = 'users.json'

    # # Initialize the users file if it doesn't exist or is empty
    # if not os.path.isfile(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
    #     with open(USERS_FILE, 'w') as f:
    #         json.dump({}, f)
    # with open(USERS_FILE, 'r') as f:
    #     users = json.load(f)
    # users = {}
    # return users


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> models.User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = schemas.TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = crud.user.get(db, id=token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_current_active_user(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user
