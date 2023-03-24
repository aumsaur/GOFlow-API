from authlib.jose import jwt


def create_access_token(data: dict, expires_in: int = 300):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data
    secret = "secret_key"
    return jwt.encode(header, payload, secret, algorithm='HS256', expires_in=expires_in)

    #jwt.decode(token, secret, algorithms=['HS256'])


def hash_password(password: str):
    hashed_password = password
    return hashed_password
