import secrets
from datetime import timedelta

from authlib.integrations.starlette_client import OAuthError

# from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps
from apps.core.config import settings
from apps.core.oauthconfig import oauth
from apps.core.security import create_access_token, get_user_from_token

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
    return "db is none"


@router.post("/register")
async def register(request: Request, db: Session = Depends(deps.get_db), newuser: schemas.UserCreate = Depends()):
    if crud.user.get_by_email(db, email=newuser.email):
        return status.HTTP_409_CONFLICT  # email already being used
    user = crud.user.create(db, obj_in=newuser)
    # return status.HTTP_201_CREATED  # should return login session instead
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # request.session['user'] = dict(user)
    return {
        "access_token": create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires
        ),
        "token_type": "bearer", "status": status.HTTP_201_CREATED
    }


@router.post("/login/access-token")
async def login_access_token(request: Request, db: Session = Depends(deps.get_db), *, email: str, password: str):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=email, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires
        ),
        "token_type": "bearer", "status": status.HTTP_200_OK
    }

# Google ###########


@router.get('/login/access-token/google')
async def login_access_token_google(request: Request):
    redirect_uri = request.url_for('authenticate_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/login/access-token/google/callback')
async def authenticate_google(request: Request, db: Session = Depends(deps.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return error.description
    if token.get('userinfo'):
        user_google = token.get('userinfo')
        if not crud.user.get_by_email(db, email=user_google.get('email')):
            created = schemas.UserCreate(
                displayname=user_google.get('given_name'),
                email=user_google.get('email'),
                user_type=schemas.UserType.google
            )
            crud.user.create(db, obj_in=created)
    user = crud.user.authenticate(
        db, email=user_google.get('email')
    )
    print(type(user))
    print(type({"sub": user}))
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires
        ),
        "token_type": "bearer", "status": status.HTTP_200_OK
    }
