from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    google = 'Google'
    app = 'App'
    other = 'Other'


class UserBase(BaseModel):
    displayname: str
    email: EmailStr

    user_type: str = UserType.app


class UserDBBase(UserBase):
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str | None = None


class UserDB(UserDBBase):
    hashed_password: str


class UserGet(UserDBBase):
    pass


class UserUpdate(UserCreate):
    pass
