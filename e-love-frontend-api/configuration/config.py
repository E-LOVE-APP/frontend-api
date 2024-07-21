# import os
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv

# load_dotenv()

# class Settings(BaseSettings):
#     API_V1_STR: str = "/api/v1"
#     PROJECT_NAME: str = "E-Love Frontend API"
#     BACKEND_CORS_ORIGINS: str = "*"
#     DATABASE_URI: str = os.getenv("DATABASE_URI")
#     SECRET_KEY: str = os.getenv("SECRET_KEY")

#     class Config:
#         env_file = ".env"

# settings = Settings()