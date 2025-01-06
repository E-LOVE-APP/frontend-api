from typing import List

from prefect import task
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for extracting users data from the database.
"""


# TODO: probably should be optimized
@task(cache_key_fn=lambda *args, **kwargs: None)
async def extract_users_task(db_session: AsyncSession) -> List[dict]:
    """
    Async task for extracting users from the database.

    params:
        db_session (AsyncSession): Database session.
    returns:
        users (List[dict]): List of users data.
    raises:
        Exception: If failed to extract users data from the database.
    """
    try:
        query = text("SELECT * FROM user")
        result = await db_session.execute(query)
        rows = result.fetchall()
        users = [dict(r._mapping) for r in rows]

        return users

    except Exception as e:
        ExceptionHandler(e)
