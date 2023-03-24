from apps.jwt import create_jwt_token
from fastapi import (
    FastAPI
)
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
    JSONResponse
)
from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError
)
from datetime import datetime, timedelta
import os
+import json


with open('client_secret.json') as f:
    client_config = json.load(f)

# Get Google client ID and client secret from secrets dict
GOOGLE_CLIENT_ID = client_config['web']['client_id']
GOOGLE_CLIENT_SECRET = client_config['web']['client_secret']

with open('localconfig.json', 'r') as f:
    config = json.load(f)

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']


USERS_FILE = 'users.json'

# Initialize the users file if it doesn't exist or is empty
if not os.path.isfile(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

app = FastAPI()

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


@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout/google">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login/google">login</a>')


@app.get('/login/google')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/login/google/callback')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        email = user.get('email')
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            if email in users:
                user_data = users[email]
            else:
                user_data = {
                    'name': user.get('name'),
                    'picture': user.get('picture'),
                    'created_at': str(datetime.utcnow())
                }
                users[email] = user_data
                with open(USERS_FILE, 'w') as f:
                    json.dump(users, f)

            token_data = {
                'email': email,
                'name': user_data['name'],
                'picture': user_data['picture'],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }

            token = create_jwt_token(
                token_data, timedelta(hours=1))

            response = JSONResponse(
                {'access_token': token, 'token_type': 'bearer'})
            response.set_cookie('token', token, httponly=True)
            return response

    return RedirectResponse(url='/')


@app.get('/logout/google/')
async def logout(request: Request):
    request.session.pop('user', None)

    return RedirectResponse(url='/')
