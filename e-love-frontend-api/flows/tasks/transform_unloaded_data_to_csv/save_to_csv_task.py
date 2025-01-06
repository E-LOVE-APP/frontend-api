import csv
from datetime import datetime
from typing import List

from prefect import task

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for saving users data to a CSV file.
"""


@task
def save_to_csv_task(users: List[dict]) -> str:
    """
    Task for saving users data to a CSV file.

    params:
        users (List[dict]): List of users data.
    returns:
        csv_path (str): Path to the saved CSV file.
    raises:
        Exception: If no users data to save to CSV.
    """
    try:
        if not users:
            raise Exception("No users data to save to CSV")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = f"data/users_{timestamp}.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)

        return csv_path
    except Exception as e:
        ExceptionHandler(e)
