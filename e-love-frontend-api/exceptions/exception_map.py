# exceptions/exception_map.py

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

# Хранение в виде - ErrorType: (status_code, message) == Dict[Type[Exception], Tuple[int, str]]
ExceptionMap: Dict[Type[Exception], Tuple[int, str]] = {
    IntegrityError: (status.HTTP_400_BAD_REQUEST, CommonExceptions.INTEGRITY_ERROR.value),
    NoResultFound: (status.HTTP_404_NOT_FOUND, CommonExceptions.RESOURCE_NOT_FOUND.value),
    ValidationError: (
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        CommonExceptions.VALIDATION_ERROR.value,
    ),
    SQLAlchemyError: (status.HTTP_500_INTERNAL_SERVER_ERROR, CommonExceptions.DATABASE_ERROR.value),
    OperationalError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.DATABASE_ERROR.value,
    ),
    DBAPIError: (status.HTTP_500_INTERNAL_SERVER_ERROR, CommonExceptions.DATABASE_ERROR.value),
    ResponseValidationError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        CommonExceptions.RESPONSE_VALIDATION_ERROR.value,
    ),
    # TODO: просмотреть на предмет большего числа исключений?
}
