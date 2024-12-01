from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

"""Pydantic схемы для ассоциации категорий пользователя."""


class AddCategoryToUser(BaseModel):
    """
    Схема для добавления категории пользователю.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        category_id (UUID): UUID категории.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    category_id: UUID = Field(..., description="UUID of the category")


class AddCategoriesToUser(BaseModel):
    """
    Схема для добавления нескольких категорий пользователю.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        category_ids (List[UUID]): Список UUID категорий для добавления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    category_ids: List[UUID] = Field(..., description="List of UUIDs of the categories to add")


class UpdateUserCategories(BaseModel):
    """
    Схема для обновления категорий пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        new_category_ids (List[UUID]): Список новых UUID категорий для назначения пользователю.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    new_category_ids: List[UUID] = Field(
        ..., description="List of new category UUIDs to assign to the user"
    )


class RemoveCategoryFromUser(BaseModel):
    """
    Схема для удаления категории у пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        category_id (UUID): UUID категории для удаления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    category_id: UUID = Field(..., description="UUID of the category to remove")


class RemoveCategoriesFromUser(BaseModel):
    """
    Схема для удаления нескольких категорий у пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        category_ids (List[UUID]): Список UUID категорий для удаления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    category_ids: List[UUID] = Field(..., description="List of UUIDs of the categories to remove")
