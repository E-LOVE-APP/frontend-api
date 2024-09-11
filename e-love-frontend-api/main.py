"""This is the main file for our application"""

import logging
from fastapi import FastAPI
from configuration.config import settings
from configuration.database import engine, Base, get_db_session
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    try:
        with get_db_session() as db:
            db.execute(text("SELECT 1"))
        logger.info("Connected to the database successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


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
