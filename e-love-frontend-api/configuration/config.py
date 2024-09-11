# config.py
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Loading .env file
load_dotenv(os.getenv("APP_ENV_PATH"))
print(f"Loaded .env path: {os.getenv('APP_ENV_PATH')}")


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_running_env: str
    greeting_message: str
    database_url: str
    alembic_database_url: Optional[str]

    class Config:
        env_file = os.getenv("APP_ENV_PATH")
        extra = "ignore"


settings = Settings()
