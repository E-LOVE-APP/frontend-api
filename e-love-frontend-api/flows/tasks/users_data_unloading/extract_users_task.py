from typing import List

from prefect import task
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for extracting users data from the database.
"""


# TODO: probably should be optimized
@task
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
        query = text("SELECT * FROM users")
        result = await db_session.execute(query)
        users = result.fetchall()
        return [dict(user) for user in users]

    except:
        ExceptionHandler(e)
