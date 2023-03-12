import os
import json

from jose import jwt
from datetime import datetime, timedelta
from typing import Dict, Any

with open('localconfig.json', 'r') as f:
    config = json.load(f)

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']


def create_access_token(data: dict, expires_in: int = 300):
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = data
    secret = SECRET_KEY
    return jwt.encode(header, payload, secret, algorithm=ALGORITHM, expires_in=expires_in)


def create_jwt_token(data: Dict[str, Any], expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
