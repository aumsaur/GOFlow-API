import json

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException

from apps.core.config import settings
from typing import Dict, Any


# with open('localconfig.json', 'r') as f:
#     config = json.load(f)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenDecodeError(Exception):
    pass


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    encoded_payload = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_payload


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError as e:
        raise TokenDecodeError("Error decoding token") from e


# TOKEN TODO:
# {
#     "sub": "{\"displayname\": \"ROMTAM\", \"email\": \"romtam.tan@mail.kmutt.ac.th\", \"user_type\": \"Google\", \"id\": \"737853f057734cf49ecd742071c743bd\"}",
#     "exp": 1682822977
# }
# 1682822977 is


def verify_access_token(token: str):
    try:
        decoded_token = decode_access_token(token)
        exp = decoded_token.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

# def is_token_expire(token: str):
#     try:
#         decoded_token = decode_access_token(token)
#         exp_timestamp = decoded_token["exp"]
#         exp_datetime = datetime.fromtimestamp(exp_timestamp)
#         return exp_datetime < datetime.now()
#     except jwt.exceptions.ExpiredSignatureError:
#         return True


def get_user_from_token(token: str):
    if token:
        try:
            user = decode_access_token(token)['name']
            return user
        except KeyError as e:
            raise TokenDecodeError(
                "Token does not contain expected key") from e
        except JWTError as e:
            raise TokenDecodeError("Error getting user from token") from e
    return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)
