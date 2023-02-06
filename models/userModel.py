from pydantic import BaseModel, EmailStr, validator

from typing import Optional

from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):  # Role/Permission in project
    owner = "owner"
    coowner = "coowner"
    member = "member"
    guest = "guest"


class Badges(str, Enum):  # Plan
    admin = "admin"
    free = "free"


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


# class Token(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

#     @validator("username", pre=True)
#     def isUsername(cls, value):
#         if value is None:
#             if cls.dict().get("email") is None:
#                 raise ValueError("email or username is required")
#         return value


class Profile(BaseModel):
    fName: str
    mName: Optional[str]
    lName: str
