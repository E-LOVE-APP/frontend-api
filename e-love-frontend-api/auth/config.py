# auth.py
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(os.getenv("APP_AUTH_ENV_PATH"))
print(f"Loaded .env path: {os.getenv('APP_AUTH_ENV_PATH')}")


class AuthSettings(BaseSettings):
    # app_secret_key: str
    # auth0_api_audience: str
    # auth0_client_id: str
    # auth0_client_secret: str
    # auth0_client_secret: str
    # auth0_domain: str
    supabase_jwt_secret: str

    class Config:
        env_file = os.getenv("APP_AUTH_ENV_PATH")
        extra = "ignore"


auth_settings = AuthSettings()  # type: ignore
