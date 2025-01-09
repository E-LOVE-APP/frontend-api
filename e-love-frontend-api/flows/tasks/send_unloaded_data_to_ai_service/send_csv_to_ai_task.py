import os

import httpx
from prefect import task

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for sending CSV file to AI service.
"""

AI_SERVICE_URL = os.getenv("AI_SERVICE_CSV_API_URL")


# TODO: change the URL to env-variable
@task
async def send_csv_to_ai_task(csv_path: str):
    """
    Send CSV file to AI service asynchronously.

    params:
        csv_path (str): Path to the
    returns:
        None
    raises:
        Exception: If failed to send CSV file to AI service.
    """
    try:
        async with httpx.AsyncClient() as client:
            with open(csv_path, "rb") as f:
                files = {"file": ("users.csv", f, "text/csv")}
                response = await client.post(AI_SERVICE_URL, files=files)
                response.raise_for_status()
    except Exception as e:
        ExceptionHandler(e)
