from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    google = 'Google'
    app = 'App'
    other = 'Other'


class UserBase(BaseModel):
    display_name: Optional[str]
    email: EmailStr

    user_type: str | None = UserType.app


class UserDBBase(UserBase):
    id: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str | None = None


class UserDB(UserDBBase):
    hashed_password: str


class UserGet(UserDBBase):
    pass


class UserProfile(BaseModel):
    display_name: str
    email: EmailStr


class UserUpdateProfile(BaseModel):
    display_name: Optional[str]
    email: Optional[EmailStr]


class UserUpdatePassword(BaseModel):
    old_password: Optional[str]
    new_password: str


class UserResetPassword(UserUpdatePassword):
    reset_token: str
