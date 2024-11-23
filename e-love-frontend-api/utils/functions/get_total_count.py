# utils/functions/get_total_count.py

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


async def get_total_count(db_session: AsyncSession, main_query: Select) -> int:
    """
    Подсчитывает количество возвращаемых сущностей из переданного запроса.

    Параметры:
        - db_session: Асинхронная сессия базы данных для выполнения запроса.
        - main_query: Запрос, из которого нужно получить количество сущностей.

    Возвращает:
        - int: Количество сущностей, возвращаемых запросом.
    """

    count_query = select(func.count()).select_from(main_query.subquery())
    total_result = await db_session.execute(count_query)
    total = total_result.scalar_one()
    return total
