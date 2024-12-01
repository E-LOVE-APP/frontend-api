from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

"""Pydantic схемы для гендера пользователя."""


class UserGenderBase(BaseModel):
    """
    Базовая схема гендера пользователя.

    Атрибуты:
        id (Optional[UUID]): ID гендера в формате UUID.
        gender_name (str): Название гендера.
    """

    id: Optional[UUID] = Field(None, description="ID of the gender in UUID format")
    gender_name: str = Field(..., max_length=50, min_length=2, description="Name of the gender")

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserGenderCreate(UserGenderBase):
    """
    Схема для создания нового гендера пользователя.
    """

    pass


class UserGenderUpdate(BaseModel):
    """
    Схема для обновления гендера пользователя.

    Атрибуты:
        gender_name (Optional[str]): Название гендера.
    """

    gender_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the gender"
    )

    model_config = ConfigDict(extra="forbid")


class UserGenderOutput(UserGenderBase):
    """
    Схема для отображения гендера пользователя.
    """

    pass
