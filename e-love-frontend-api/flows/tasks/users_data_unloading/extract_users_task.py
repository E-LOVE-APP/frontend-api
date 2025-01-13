from typing import List

import pandas as pd
from prefect import task
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for extracting users data from the database.
"""


# TODO: probably should be optimized
@task
async def extract_users_task(db_session: AsyncSession) -> pd.DataFrame:
    """
    Задача для подготовки данных для обучения модели рекомендаций.
    Возвращает DataFrame с колонками: current_user_id, candidate_user_id, categories, description, liked.
    """
    try:
        sql = text(
            """
            SELECT 
                u1.id AS current_user_id,
                u2.id AS candidate_user_id,
                GROUP_CONCAT(c.category_name) AS categories,
                u2.user_descr AS description,
                CASE 
                    WHEN ui.interaction_type = 'MATCH' THEN 1 
                    ELSE 0 
                END AS liked
            FROM user u1
            CROSS JOIN user u2
            LEFT JOIN user_categories uc ON u2.id = uc.user_id
            LEFT JOIN categories c ON c.id = uc.category_id
            LEFT JOIN user_interaction ui 
                ON ui.user_id = u1.id 
               AND ui.target_user_id = u2.id 
               AND ui.interaction_type = 'MATCH'
            WHERE u1.id != u2.id
            GROUP BY u1.id, u2.id
            """
        )
        result = await db_session.execute(sql)
        rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]
        df = pd.DataFrame(data)

        if "categories" in df.columns:
            df["categories"] = (
                df["categories"].fillna("").apply(lambda x: x.split(",") if x else [])
            )

        return df

    except Exception as e:
        ExceptionHandler(e)
