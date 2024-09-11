"""Database configuration."""

# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from configuration.config import settings
from dotenv import load_dotenv
import os
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# load_dotenv(dotenv_path="/app/docker/db-app/db.env")

DATABASE_URL = settings.database_url
ALEMBIC_DATABASE_URL = settings.alembic_database_url

if not DATABASE_URL:
    logging.error("DATABASE_URL is not set in environment variables.")
    raise ValueError("DATABASE_URL must be set in environment variables.")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logging.error(f"Failed to connect to database: {e}")
    raise

Base = declarative_base()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        # TODO: check why do we use yield here!!
        yield db
    except Exception as e:
        logging.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
