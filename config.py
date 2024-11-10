# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE') or None
DISCOVERY_URL = f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
SECRET_KEY = os.getenv('SECRET_KEY')

