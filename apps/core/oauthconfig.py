from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from apps.core.config import settings

# Setup OAuth Google
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
