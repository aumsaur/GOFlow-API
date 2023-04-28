from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow

from apps.core.config import settings

# Setup OAuth Google
config_data = {'GOOGLE_CLIENT_ID': settings.CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': settings.CLIENT_SECRET}
starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# SCOPE = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
#          'https://www.googleapis.com/auth/userinfo.profile']

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# flow = Flow.from_client_config(
#     client_config={
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uris": settings.REDIRECT_URIS,
#         "scopes": SCOPE,
#     },
#     scopes=SCOPE,
# )
