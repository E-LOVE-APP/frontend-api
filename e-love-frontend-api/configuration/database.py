# database.py

import contextlib
import logging
from typing import AsyncGenerator

import colorlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

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

if not DATABASE_URL:
    logger.error("DATABASE_URL is not set in environment variables.")
    raise ValueError("DATABASE_URL must be set in environment variables.")

try:
    engine = create_async_engine(DATABASE_URL)
    # AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    logger.info("Async SQLAlchemy engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create async SQLAlchemy engine: {e}")
    raise

Base = declarative_base()
logger.info("Starting database connection check...")


AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# @asynccontextmanager
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception as e:
#             await session.rollback()
#             logger.error(f"Database session error: {e}")
#             raise

import contextlib
import logging
import traceback
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from configuration.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def handle_session_exception(session: AsyncSession, exc: BaseException):
    """
    Общая утилита, вызываемая при ошибках в сессии:
    - делаем rollback
    - логируем traceback
    """
    logger.error(f"Exception in session: {exc}\n{traceback.format_exc()}")
    await session.rollback()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """ """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()
