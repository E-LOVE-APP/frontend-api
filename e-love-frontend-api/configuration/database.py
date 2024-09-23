"""Database configuration."""

import logging
from contextlib import contextmanager

import colorlog
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configuration.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

DATABASE_URL = settings.database_url
# UC-9:  В ошибке вижу отсутсвие в этом файле ALEMBIC_DATABASE_URL(его тут и нет), поэтому сделаю такое решение
ALEMBIC_DATABASE_URL = DATABASE_URL 

if not DATABASE_URL:
    logger.error("DATABASE_URL is not set in environment variables.")
    raise ValueError("DATABASE_URL must be set in environment variables.")

# Настройка SQLAlchemy
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SQLAlchemy engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create SQLAlchemy engine: {e}")
    raise

Base = declarative_base()


# Проверка подключения при загрузке конфигурации
def check_db_connection():
    """Проверяет подключение к базе данных при загрузке конфигурации"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Connected to the database successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise


logger.info("Starting database connection check...")

check_db_connection()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
