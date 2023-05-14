from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException

from apps.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenDecodeError(Exception):
    pass


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Create an access token with the provided data and expiration delta.

    Args:
        data (dict): The data to include in the access token payload.
        expires_delta (timedelta, optional): The expiration delta for the access token. Defaults to timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns:
        str: The encoded access token.

    Raises:
        None
    """
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    encoded_payload = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_payload


def decode_access_token(token: str):
    """
    Decode and verify an access token.

    Args:
        token (str): The access token to decode and verify.

    Returns:
        dict: The payload of the decoded access token.

    Raises:
        TokenDecodeError: If there is an error decoding the token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError as e:
        raise TokenDecodeError("Error decoding token") from e


def verify_access_token(token: str):
    """
    Verify the access token and return the expiration time as a `datetime` object if the token is valid.

    Args:
        token (str): The access token to verify.

    Returns:
        datetime: The expiration time of the token as a `datetime` object if the token is valid.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    try:
        decoded_token = decode_access_token(token)
        exp = decoded_token.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token expire")
        return datetime.fromtimestamp(exp)
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")


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
