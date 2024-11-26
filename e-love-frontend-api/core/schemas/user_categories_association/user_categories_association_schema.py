from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class AddCategoryToUser(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    category_id: UUID = Field(..., description="UUID of the category")


class AddCategoriesToUser(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    category_ids: List[UUID] = Field(..., description="List of UUIDs of the category to add")


class UpdateUserCategories(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    new_category_ids: List[UUID] = Field(
        ..., description="List of new categories UUIDs to assign to the user"
    )


class RemoveCategoryFromUser(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    category_id: UUID = Field(..., description="UUID of the category to remove")


class RemoveCategoriesFromUser(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    category_ids: List[UUID] = Field(..., description="List of UUIDs of the categories to remove")
