import secrets
from datetime import timedelta

from authlib.integrations.starlette_client import OAuthError

# from starlette.middleware.sessions import SessionMiddleware
# from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    Depends
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps
from apps.core.config import settings
# from apps.core.oauthconfig import oauth
from apps.core.security import create_access_token, decode_access_token, get_hashed_password

router = APIRouter()

# App ###########


@router.get("/")
async def home(db: Session = Depends(deps.get_db)):

    if not db:
        print(db)
        try:
            return db
        except:
            return "cant return db"
    return db


@router.post("/register")
async def register(request: Request, db: Session = Depends(deps.get_db), *, newuser: schemas.UserCreate = Depends()):
    if crud.user.get_by_email(db, email=newuser.email):
        # email already being used
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already used")
    user = crud.user.create(db, obj_in=newuser)

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {
        "access_token": create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires
        ),
        "token_type": "bearer", "status": status.HTTP_201_CREATED
    }
    # request.session['access_token'] = access_token
    return access_token


@router.post("/login/access-token")
async def login_access_token(request: Request, db: Session = Depends(deps.get_db), *, email: str, password: str):
    user = crud.user.authenticate(
        db, email=email, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {
        {
            "access_token": create_access_token(
                {"sub": user.json()}, expires_delta=access_token_expires
            ),
            "token_type": "bearer", "status": status.HTTP_200_OK
        }
    }
    # request.session['access_token'] = access_token
    return access_token


# Google ###########

# {
# "id": "109518956227943178476",

# TODO: "email": "romtam.tan@mail.kmutt.ac.th",

# "verified_email": true,
# "name": "ROMTAM TANPITUCKPONG",

# TODO: "given_name": "ROMTAM",

# "family_name": "TANPITUCKPONG",
# "picture": "https://lh3.googleusercontent.com/a/AGNmyxYHvnb4Av7lWxqyBELi4uaJYS3z0rvItFkjgwS0=s96-c",
# "locale": "en", "hd": "mail.kmutt.ac.th"
# }


@router.post('/login-google/access-token')
async def authenticate_google(request: Request, db: Session = Depends(deps.get_db), *, token: dict):
    if not crud.user.get_by_email(db, email=token.get('email')):
        created = schemas.UserCreate(
            displayname=token.get('given_name'),
            email=token.get('email'),
            user_type=schemas.UserType.google
        )
        crud.user.create(db, obj_in=created)
    user = crud.user.authenticate(
        db, email=token.get('email'), type=schemas.UserType.google
    )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {
        "access_token": create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires
        ),
        "token_type": "bearer", "status": status.HTTP_200_OK
    }
    return access_token


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('access_token', None)

# google login api which is popup instead of redirect to google login page with fastapi

# TOKEN
# {
#     "sub": "{\"displayname\": \"ROMTAM\", \"email\": \"romtam.tan@mail.kmutt.ac.th\", \"user_type\": \"Google\", \"id\": \"737853f057734cf49ecd742071c743bd\"}",
#     "exp": 1682822977
# }
# 1682822977 is


@router.get('/decode-token')
async def decode_token(token: str):
    return decode_access_token(token)


@router.delete('/delete')
async def delete_user(db: Session = Depends(deps.get_db), *, id: str):
    return crud.user.remove(db, id=id)


@router.get('/fetch')
async def fetch_user(db: Session = Depends(deps.get_db), *, email: str):
    return crud.user.get_by_email(db, email=email)
