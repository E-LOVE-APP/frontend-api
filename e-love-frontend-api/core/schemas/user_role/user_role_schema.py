from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

"""Pydantic схемы для ролей пользователей."""


class UserRoleBase(BaseModel):
    """
    Базовая схема роли пользователя.

    Атрибуты:
        id (Optional[UUID]): ID роли в формате UUID.
        role_name (str): Название роли.
    """

    id: Optional[UUID] = Field(None, description="ID of the role in UUID format")
    role_name: str = Field(..., max_length=50, min_length=4, description="Name of the role")

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserRoleCreate(UserRoleBase):
    """
    Схема для создания новой роли пользователя.
    """

    pass


class UserRoleUpdate(BaseModel):
    """
    Схема для обновления роли пользователя.

    Атрибуты:
        role_name (Optional[str]): Название роли.
    """

    role_name: Optional[str] = Field(
        None, max_length=50, min_length=4, description="Name of the role"
    )

    model_config = ConfigDict(extra="forbid")


class UserRoleOutput(UserRoleBase):
    """
    Схема для отображения роли пользователя.
    """

    pass
