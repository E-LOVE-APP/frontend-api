from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

"""Pydantic схемы для категорий пользователей."""


class CategoryOutput(BaseModel):
    """
    Схема для отображения данных категории.

    Атрибуты:
        id (UUID): ID категории в формате UUID.
        category_name (str): Название категории.
        category_descr (str): Описание категории.
        category_icon (Optional[str]): Иконка категории.
    """

    id: UUID = Field(..., description="ID of the category in UUID format")
    category_name: str = Field(..., description="Name of the category")
    category_descr: str = Field(..., description="Description of the category")
    category_icon: Optional[str] = Field(None, description="Icon of the category")

    model_config = ConfigDict(from_attributes=True, extra="forbid")
