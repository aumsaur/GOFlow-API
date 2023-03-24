from apps.core.security import create_jwt_token
from fastapi import (
    APIRouter
)
from starlette.config import Config
from starlette.requests import Request
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
import json

from apps.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

app = APIRouter()

config_data = {'GOOGLE_CLIENT_ID': settings.CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': settings.CLIENT_SECRET}
starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

users = {
    "deityts.tg@gmail.com": {
        "name": "Chlarm Chlarm",
        "picture": "https://lh3.googleusercontent.com/a/AGNmyxZXBcl53455hPo-Z3omV9_RZS8n1EsF85TLaBuh7w=s96-c",
        "created_at": "2023-03-12 17:05:47.326128"
    },
}


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


@app.get('/login/access-token/google')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    # debug = await oauth.google.authorize_redirect(request, redirect_uri)
    # print(debug)
    # return await oauth.google.authorize_redirect(request, redirect_uri, display = 'popup')
    auth_url = await oauth.google.create_authorization_url(redirect_uri=redirect_uri)
    # print(result)
    script = f"""
        <script>
            window.open("{auth_url.get('url')}", "google-login", "height=600,width=600");
            window.close();
        </script>
    """
    return HTMLResponse(content=script, status_code=200)


@app.get('/login/access-token/google/callback')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        print(error)
    user = token.get('userinfo')
    if user:
        email = user.get('email')
        if email in users:
            user_data = users[email]
        else:
            user_data = {
                'name': user.get('name'),
                'picture': user.get('picture'),
                'created_at': str(datetime.utcnow())
            }
            users[email] = user_data

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
        print(response)

    return RedirectResponse(url='/')


@app.get('/logout/google/')
async def logout(request: Request):
    request.session.pop('user', None)

    return RedirectResponse(url='/')
