# utils/enums/common_exceptions.py

"""
Модуль содержит перечисление CommonExceptions с общими сообщениями об ошибках,
используемыми в приложении.
"""

from enum import Enum


class CommonExceptions(Enum):
    """
    Перечисление стандартных сообщений об ошибках для использования в ответах API.
    """

    # 300-е коды
    MOVED_PERMANENTLY = "The resource has been moved permanently."

    # 400-е коды
    BAD_REQUEST = "Bad request."
    VALIDATION_ERROR = "Validation error."
    INTEGRITY_ERROR = "Integrity constraint violated."
    UNIQUE_CONSTRAINT_VIOLATION = "A unique constraint was violated."
    FOREIGN_KEY_CONSTRAINT_VIOLATION = "A foreign key constraint was violated."
    AUTHENTICATION_FAILED = "Authentication failed."
    AUTHORIZATION_FAILED = "Authorization failed."
    FORBIDDEN_ERROR = "Access forbidden."
    RESOURCE_NOT_FOUND = "Resource not found."
    CONFLICT_ERROR = "A conflict occurred."
    UNSUPPORTED_MEDIA_TYPE = "Unsupported media type."
    TOO_MANY_REQUESTS = "Too many requests."

    # 500-е коды
    DATABASE_ERROR = "A database error occurred."
    UNEXPECTED_ERROR = "An unexpected error occurred."
    RESPONSE_VALIDATION_ERROR = (
        "Input should be a valid dictionary or object to extract fields from."
    )
    TIMEOUT_ERROR = "The server timed out waiting for the request."
    NOT_IMPLEMENTED_ERROR = "This functionality is not implemented."
