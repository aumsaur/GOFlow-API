import json

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from config import settings


with open('localconfig.json', 'r') as f:
    config = json.load(f)

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    encoded_payload = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_payload


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError:
        return None


async def get_user_from_token(token: str):
    if token:
        try:
            user = decode_access_token(token)['name']
            return user
        except:
            pass
    return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)
