# exceptions/custom_exceptions.py

import logging
from typing import Type

from fastapi import HTTPException, status

from exceptions.exception_map import ExceptionMap
from utils.enums.common_exceptions import CommonExceptions

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """
    Класс для преобразования различных исключений в HTTPException с соответствующими статусами и сообщениями.
    """

    def __init__(self, exception: Exception):
        """
        Инициализация ExceptionHandler с преобразованием исходного исключения в HTTPException.

        :param exc: Исходное исключение
        :raises HTTPException: Преобразованное HTTPException
        """

        http_exception = self.map_exception(exception=exception)

        if http_exception:
            raise http_exception

        else:
            # Если исключение не найдено в маппинге, поднимаем общий Internal Server Error
            logger.error(f"Unhandled exception: {exception}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CommonExceptions.UNEXPECTED_ERROR.value,
            )

    def map_exception(self, exception: Exception) -> HTTPException:
        """
        Преобразует переданное исключение в соответствующий HTTPException.

        :param exception: Исходное исключение
        :return: HTTPException или None, если тип исключения не обработан
        """
        for exception_type, (status_code, message) in ExceptionMap.items():
            if isinstance(exception, exception_type):
                # Обработка подтипов исключений, если необходимо
                if exception_type == IntegrityError:
                    error_str = str(exception.orig).lower()
                    if "unique constraint" in error_str:
                        message = CommonExceptions.UNIQUE_CONSTRAINT_VIOLATION.value
                    elif "foreign key constraint" in error_str:
                        message = CommonExceptions.FOREIGN_KEY_CONSTRAINT_VIOLATION.value
                # Если статус код не задан (например, для HTTPException), используем из маппинга
                if status_code:
                    return HTTPException(status_code=status_code, detail=message)
                else:
                    # Если статус код не задан, предполагаем, что исключение само по себе HTTPException
                    if isinstance(exception, HTTPException):
                        return exception
        return None
