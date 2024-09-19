"""This is the main file for our application"""

import logging

from fastapi import FastAPI
from sqlalchemy import text

from configuration.config import settings
from configuration.database import Base, engine, get_db_session
from easter_eggs.greeting import ascii_hello_devs, ascii_kitty, ascii_painter

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Create the database tables
Base.metadata.create_all(bind=engine)

print(ascii_hello_devs)
print(ascii_painter)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


# Test routes. We will remove these later
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
