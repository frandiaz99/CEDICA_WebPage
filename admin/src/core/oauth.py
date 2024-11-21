# src/core/extensions.py
from authlib.integrations.flask_client import OAuth

oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=None,  # Se establecerán en la inicialización del app
    client_secret=None,
    server_metadata_url= None,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    client_kwargs={
        'scope': 'openid email profile',
    },
)
