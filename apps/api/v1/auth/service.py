import json
import os
from datetime import datetime, timedelta

from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError
)

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)

from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps
from apps.core.config import settings
from apps.core.oauthconfig import oauth
from apps.core.secure import create_access_token, get_user_from_token

router = APIRouter()

# App ###########


@router.post("/register")
async def register(db: Session = Depends(deps.get_db), newuser: schemas.UserCreate = Depends()):
    if crud.user.get_by_email(db, email=newuser.email):
        return status.HTTP_409_CONFLICT  # email already being used
    crud.user.create(db, obj_in=newuser)
    return status.HTTP_201_CREATED  # should return login session instead


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(db: Session = Depends(deps.get_db), *, email: str, password: str):
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
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

# Google ###########


@router.get('/login/access-token/google')
async def login_access_token_google(request: Request):
    redirect_uri = request.url_for('authenticate_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get('/login/access-token/google/callback')
# async def authenticate_google(request: Request, db: Session = Depends(deps.get_db)):

@router.get('/login/access-token/google/callback')
async def authenticate_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        print(error)
        return
    # token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        email = user.get('email')
    print(email + ';email')
    print('\n;email')
    return email
    # userinfo = json.dumps(token.get('userinfo'))
    # return userinfo + '\n; ' + user + '\n;' + token.get('userinfo')
    # if not crud.user.get_by_email(db, email=user.get('email')):
    #     created = schemas.UserCreate(displayname=user.get('name').replace(' ', ''), email=user.get('email'),
    #                                  user_type=schemas.UserType.google)
    #     # crud.user.create(db, obj_in=user)
    #     print(created)


# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# # JWT helper function
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # OpenAPI documentation


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="My API",
#         version="0.1.0",
#         description="This is my API",
#         routes=app.routes,
#     )
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
#     return current_user


# @app.post("/user/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["users"], summary="Register")
# async def create_user(user_in: UserIn):
#     if not get_user(user_in.username):  # not exist in database
#         user_saved = fake_save_user(user_in)
#         return user_saved
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")


# @app.post("user/token/login", response_model=Token, status_code=status.HTTP_200_OK, tags=["users"], summary="Login")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(
#         form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/all/", response_model=dict[str, User], tags=["debug"])
# async def read_users_all():
#     return fake_users_db


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
