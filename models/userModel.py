from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None

    # @property
    # def email(self):
    #     return self._email

    # @email.setter
    # def email(self, value):
    #     if value is None:
    #         self._email = f"{self.username}@mail.com"
    #     elif isinstance(value, str) and "@" in value:
    #         self._email = value
    #     else:
    #         raise ValueError("Invalid email address")


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class User(UserBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
