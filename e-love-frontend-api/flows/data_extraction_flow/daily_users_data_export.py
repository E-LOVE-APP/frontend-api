import logging

import httpx
from prefect import flow

from exceptions.exception_handler import ExceptionHandler
from flows.db_context.get_db_context import create_db_context
from flows.tasks.send_unloaded_data_to_ai_service.send_csv_to_ai_task import send_csv_to_ai_task
from flows.tasks.transform_unloaded_data_to_csv.save_to_csv_task import save_to_csv_task
from flows.tasks.users_data_unloading.extract_users_task import extract_users_task

"""
Daily users data export flow.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: добавить более нормальные комменты (дока)
@flow(name="Daily Export Flow", log_prints=True)
async def daily_export_flow():
    """
    Async Prefect flow for daily users data export.
    """
    async with create_db_context() as session:
        users = await extract_users_task(session)
        csv_path = save_to_csv_task(users)
        await send_csv_to_ai_task(csv_path)
        logger.info("Daily users data export completed.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(daily_export_flow())
