# from sqlalchemy.orm import Session
# from pydantic import ValidationError
# from jose import jwt
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, status
# from typing import Generator
# from fastapi.encoders import jsonable_encoder
# from schemas.user import (
#     User,
#     UserCreate
# )

# from core.secure import get_hashed_password

# import crud
# import schemas
# from core.config import settings
# from models import userModel

from core.secure import get_hashed_password
from schemas.user import UserCreate, UserDB
from fastapi.encoders import jsonable_encoder
from session import session


# def fake_save_user(user_in: UserCreate):
#     hashed_password = get_hashed_password(user_in.password)
#     user_in_db = UserDB(**user_in.dict(), hashed_password=hashed_password)
#     # fake_users_db[user_in_db.username] = jsonable_encoder(user_in_db)
#     session.add(user_in)
#     return user_in_db


# def get_user(username: str):
#     if username in fake_users_db:
#         user_dict = fake_users_db[username]
#         return UserDB(**user_dict)


# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token"
# )


# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> userModel.User:
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
#     current_user: userModel.User = Depends(get_current_user),
# ) -> userModel.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: userModel.User = Depends(get_current_user),
# ) -> userModel.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user
