# utils/enums/common_exceptions.py

from enum import Enum


class CommonExceptions(Enum):
    INTEGRITY_ERROR = "Integrity constraint violated."
    UNIQUE_CONSTRAINT_VIOLATION = "A unique constraint was violated."
    FOREIGN_KEY_CONSTRAINT_VIOLATION = "A foreign key constraint was violated."
    RESOURCE_NOT_FOUND = "Resource not found."
    DATABASE_ERROR = "A database error occurred."
    VALIDATION_ERROR = "Validation error."
    AUTHENTICATION_FAILED = "Authentication failed."
    AUTHORIZATION_FAILED = "Authorization failed."
    UNEXPECTED_ERROR = "An unexpected error occurred."
    RESPONSE_VALIDATION_ERROR = (
        "Input should be a valid dictionary or object to extract fields from."
    )
