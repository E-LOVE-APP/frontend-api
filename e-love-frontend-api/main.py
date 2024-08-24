"""This is the main file for our application"""

from fastapi import FastAPI
from configuration.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/hello")
async def hello():
    """This is a test route"""
    return {"message": "Hello, World!"}


@app.get("/config-info")
async def config_info():
    """This route returns the configuration information"""
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_running_env": settings.app_running_env,
        "greeting_message": settings.greeting_message,
    }
