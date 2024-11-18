# exceptions/custom_exceptions.py

"""
Модуль содержит класс ExceptionHandler для преобразования различных исключений
в HTTPException с соответствующими статусами и детализированными сообщениями.
"""

import logging
from typing import Any, Dict, Optional, Type

from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from exceptions.exception_map import ExceptionMap
from utils.enums.common_exceptions import CommonExceptions

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """
    Класс для преобразования различных исключений в HTTPException с соответствующими статусами
    и детализированными сообщениями об ошибках.

    При инициализации принимает исключение и пытается сопоставить его с известными типами исключений.
    Если совпадение найдено, преобразует его в HTTPException с подробной информацией.
    """

    def __init__(self, exception: Exception):
        """
        Инициализация ExceptionHandler с преобразованием исходного исключения.

        :param exception: Исключение, которое нужно обработать.
        :raises HTTPException: Преобразованное исключение с соответствующим статусом и сообщением.
        """
        http_exception = self.map_exception(exception=exception)

        if http_exception:
            raise http_exception
        else:
            # Если исключение не найдено в маппинге, поднимаем общий Internal Server Error
            logger.error(f"Unhandled exception: {exception}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "errors": [
                        {
                            "type": "InternalServerError",
                            "msg": CommonExceptions.UNEXPECTED_ERROR.value,
                            "detail": str(exception),
                        }
                    ]
                },
            )

    # TODO: Вова - необходимо отрефакторить этот метод, путем создания множества мини-функций под каждый кейс из текущих if/elif-блоков и вызова их тут просто в одну строку. Я тебе открою тикет.
    def map_exception(self, exception: Exception) -> Optional[HTTPException]:
        """
        Сопоставляет исключение с известными типами и возвращает соответствующий HTTPException.

        :param exception: Исключение для сопоставления.
        :return: HTTPException с детализированным сообщением или None, если не найдено совпадение.
        """
        for exc_type, (status_code, message) in ExceptionMap.items():
            if isinstance(exception, exc_type):
                error_detail = {
                    "errors": [
                        {
                            "type": exc_type.__name__,
                            "msg": message,
                            "detail": str(exception),
                        }
                    ]
                }

                # Специальная обработка для некоторых исключений
                if isinstance(exception, ValidationError):
                    # Используем формат ошибок Pydantic
                    error_detail = {"errors": exception.errors()}
                elif isinstance(exception, IntegrityError):
                    error_str = str(exception.orig).lower()
                    if "unique constraint" in error_str:
                        message = CommonExceptions.UNIQUE_CONSTRAINT_VIOLATION.value
                    elif "foreign key constraint" in error_str:
                        message = CommonExceptions.FOREIGN_KEY_CONSTRAINT_VIOLATION.value
                    error_detail = {
                        "errors": [
                            {
                                "type": "IntegrityError",
                                "msg": message,
                                "detail": error_str,
                            }
                        ]
                    }
                elif isinstance(exception, KeyError):
                    error_detail = {
                        "errors": [
                            {
                                "type": "KeyError",
                                "msg": message,
                                "detail": f"Missing key: {str(exception)}",
                            }
                        ]
                    }
                elif isinstance(exception, ValueError):
                    error_detail = {
                        "errors": [
                            {
                                "type": "ValueError",
                                "msg": message,
                                "detail": str(exception),
                            }
                        ]
                    }
                elif isinstance(exception, PermissionError):
                    error_detail = {
                        "errors": [
                            {
                                "type": "PermissionError",
                                "msg": message,
                                "detail": str(exception),
                            }
                        ]
                    }
                elif isinstance(exception, FileNotFoundError):
                    error_detail = {
                        "errors": [
                            {
                                "type": "FileNotFoundError",
                                "msg": message,
                                "detail": f"File not found: {str(exception.filename)}",
                            }
                        ]
                    }

                return HTTPException(status_code=status_code, detail=error_detail)

        return None
