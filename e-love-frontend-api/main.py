"""This is the main file for our application"""

from fastapi import FastAPI
from configuration.config import settings
from configuration.database import engine, Base, get_db_session

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Test connection to the database
def test_db_connection():
    """Test database connection"""
    try:
        with get_db_session() as db:
            db.execute("SELECT 1")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise
    print("Connected to the database successfully")

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

if __name__ == "__main__":
    test_db_connection()