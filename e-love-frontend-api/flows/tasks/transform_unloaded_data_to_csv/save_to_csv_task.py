import csv
from datetime import datetime
from typing import List

import pandas as pd
from prefect import task

from exceptions.exception_handler import ExceptionHandler

"""
Prefect task for saving users data to a CSV file.
"""


@task
def save_to_csv_task(users_df: pd.DataFrame) -> str:
    """
    Сохраняет DataFrame пользователей в CSV.
    Если DataFrame пуст, выбрасывает Exception.
    """
    try:
        if users_df.empty:
            raise Exception("No users data to save to CSV")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = f"data/users_{timestamp}.csv"

        users_df.to_csv(csv_path, index=False, encoding="utf-8")
        return csv_path

    except Exception as e:
        ExceptionHandler(e)
