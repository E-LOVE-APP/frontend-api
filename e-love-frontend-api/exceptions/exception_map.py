# exceptions/exception_map.py

from typing import Dict, Tuple, Type

from fastapi import status
from pydantic import ValidationError
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
    NoResultFound,
    OperationalError,
    SQLAlchemyError,
)

from utils.enums.common_exceptions import CommonExceptions

ExceptionMap: Dict[Type[Exception], Tuple[int, str]] = {
    IntegrityError: (status.HTTP_400_BAD_REQUEST, CommonExceptions.INTEGRITY_ERROR),
    NoResultFound: (status.HTTP_404_NOT_FOUND, CommonExceptions.RESOURCE_NOT_FOUND),
    ValidationError: (status.HTTP_422_UNPROCESSABLE_ENTITY, CommonExceptions.VALIDATION_ERROR),
    SQLAlchemyError: (status.HTTP_500_INTERNAL_SERVER_ERROR, CommonExceptions.DATABASE_ERROR),
    OperationalError: (status.HTTP_500_INTERNAL_SERVER_ERROR, CommonExceptions.DATABASE_ERROR),
    DBAPIError: (status.HTTP_500_INTERNAL_SERVER_ERROR, CommonExceptions.DATABASE_ERROR),
    # TODO: просмотреть на предмет большего числа исключений?
}
