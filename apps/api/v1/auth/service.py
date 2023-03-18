import json
import os
from datetime import datetime, timedelta

from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError
)

# from starlette.responses import (
#     HTMLResponse,
#     RedirectResponse,
#     JSONResponse
# )

# from azure.session import fake_users_db

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.config import Config

from fastapi import (
    FastAPI,
    APIRouter,
    HTTPException,
    status,
    Depends
)

from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps

from core.secure import create_access_token, get_user_from_token, decode_jwt_token


with open('client_secret.json') as f:
    client_config = json.load(f)

# Get Google client ID and client secret from secrets dict
GOOGLE_CLIENT_ID = client_config['web']['client_id']
GOOGLE_CLIENT_SECRET = client_config['web']['client_secret']

with open('localconfig.json') as f:
    config = json.load(f)

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']


# USERS_FILE = 'users.json'

# Initialize the users file if it doesn't exist or is empty
# if not os.path.isfile(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
#     with open(USERS_FILE, 'w') as f:
#         json.dump({}, f)

router = APIRouter()
app = FastAPI()

# Setup OAuth Google
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/google/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/token', response_model=schemas.Token)
async def authenticate(request: Request, db: Session = Depends(deps.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return error
    user = token.get('userinfo')
    # if not crud.user.authenticate(db, email=user.get('email')):
    #     raise HTTPException(
    #         status_code=400, detail="Incorrect email or password")
    # elif not crud.user.is_active(user):
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            # user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
    #     if email in db:  # check if it exist in database
    #         user_data = users[email]
    #     else:  # register to database if not
    #         user_data = {
    #             'name': user.get('name'),
    #             'picture': user.get('picture'),
    #             'created_at': str(datetime.utcnow())
    #         }
    #         users[email] = user_data
    #         # with open(USERS_FILE, 'w') as f:
    #         #     json.dump(users, f)

    #     token_data = {
    #         'email': email,
    #         'name': user_data['name'],
    #         'picture': user_data['picture'],
    #         'exp': datetime.utcnow() + timedelta(seconds=30)
    #     }

    #     token = create_access_token(token_data, timedelta(seconds=30))
    #     request.session['token'] = token
    #     return token


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

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
