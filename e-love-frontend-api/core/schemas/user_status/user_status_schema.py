from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

"""Pydantic схемы для статусов пользователей."""


class UserStatusBase(BaseModel):
    """
    Базовая схема статуса пользователя.

    Атрибуты:
        id (Optional[UUID]): ID статуса пользователя в формате UUID.
        status_name (str): Название статуса пользователя.
    """

    id: Optional[UUID] = Field(None, description="ID of the user status in UUID format")
    status_name: str = Field(
        ..., max_length=50, min_length=2, description="Name of the user status"
    )

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserStatusCreate(UserStatusBase):
    """
    Схема для создания нового статуса пользователя.
    """

    pass


class UserStatusUpdate(BaseModel):
    """
    Схема для обновления статуса пользователя.

    Атрибуты:
        status_name (Optional[str]): Название статуса пользователя.
    """

    status_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the user status"
    )

    model_config = ConfigDict(extra="forbid")


class UserStatusOutput(UserStatusBase):
    """
    Схема для отображения статуса пользователя.
    """

    pass
