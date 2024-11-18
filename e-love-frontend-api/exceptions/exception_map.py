# exceptions/exception_map.py

"""
Модуль содержит карту сопоставления исключений с соответствующими HTTP статусами и сообщениями.

ExceptionMap используется в ExceptionHandler для преобразования исключений в HTTPException.
"""

from typing import Dict, Tuple, Type

from fastapi import status
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
    NoResultFound,
    OperationalError,
    SQLAlchemyError,
)

from utils.enums.common_exceptions import CommonExceptions


# Определение пользовательских исключений, если они не существуют. Возможно мы по-особому их реализуем, если они нам когда-нибудь понадобяться.
# Именно потому-что они могут нам понадобиться, я их сюда и добавил. Однако так делать не очень желательно, лучше декомпозировать на отдельные папки и импортировать просто в модуль, как из fastapi.
# TODO: Вова, я создам для тебя тикет по рефактору этого файла. Твоя задача будет просто распределить эти кастомные ошибки по папкам и импортировать сюда как обычный импорт, чтобы они не занимали лишнее пространство.
class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации."""

    pass


class AuthorizationError(Exception):
    """Исключение для ошибок авторизации."""

    pass


class ConflictError(Exception):
    """Исключение для конфликтных ситуаций (409 Conflict)."""

    pass


class UnsupportedMediaTypeError(Exception):
    """Исключение для неподдерживаемого типа медиа (415 Unsupported Media Type)."""

    pass


class TooManyRequestsError(Exception):
    """Исключение для превышения лимита запросов (429 Too Many Requests)."""

    pass


# Карта исключений: Исключение -> (HTTP статус, Сообщение)
ExceptionMap: Dict[Type[Exception], Tuple[int, str]] = {
    # 300-е коды (перенаправления)
    NotImplementedError: (
        status.HTTP_301_MOVED_PERMANENTLY,
        CommonExceptions.MOVED_PERMANENTLY.value,
    ),
    # 400-е коды (клиентские ошибки)
    ValidationError: (
        status.HTTP_400_BAD_REQUEST,
        CommonExceptions.VALIDATION_ERROR.value,
    ),
    ValueError: (
        status.HTTP_400_BAD_REQUEST,
        CommonExceptions.BAD_REQUEST.value,
    ),
    KeyError: (
        status.HTTP_400_BAD_REQUEST,
        CommonExceptions.BAD_REQUEST.value,
    ),
    IntegrityError: (
        status.HTTP_400_BAD_REQUEST,
        CommonExceptions.INTEGRITY_ERROR.value,
    ),
    PermissionError: (
        status.HTTP_403_FORBIDDEN,
        CommonExceptions.FORBIDDEN_ERROR.value,
    ),
    FileNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        CommonExceptions.RESOURCE_NOT_FOUND.value,
    ),
    NoResultFound: (
        status.HTTP_404_NOT_FOUND,
        CommonExceptions.RESOURCE_NOT_FOUND.value,
    ),
    # 401 и 403 ошибки
    AuthenticationError: (
        status.HTTP_401_UNAUTHORIZED,
        CommonExceptions.AUTHENTICATION_FAILED.value,
    ),
    AuthorizationError: (
        status.HTTP_403_FORBIDDEN,
        CommonExceptions.AUTHORIZATION_FAILED.value,
    ),
    # 409 Conflict
    ConflictError: (
        status.HTTP_409_CONFLICT,
        CommonExceptions.CONFLICT_ERROR.value,
    ),
    # 415 Unsupported Media Type
    UnsupportedMediaTypeError: (
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        CommonExceptions.UNSUPPORTED_MEDIA_TYPE.value,
    ),
    # 429 Too Many Requests
    TooManyRequestsError: (
        status.HTTP_429_TOO_MANY_REQUESTS,
        CommonExceptions.TOO_MANY_REQUESTS.value,
    ),
    # 500-е коды (ошибки сервера)
    SQLAlchemyError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.DATABASE_ERROR.value,
    ),
    OperationalError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.DATABASE_ERROR.value,
    ),
    DBAPIError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.DATABASE_ERROR.value,
    ),
    ResponseValidationError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.RESPONSE_VALIDATION_ERROR.value,
    ),
    TimeoutError: (
        status.HTTP_504_GATEWAY_TIMEOUT,
        CommonExceptions.TIMEOUT_ERROR.value,
    ),
}
