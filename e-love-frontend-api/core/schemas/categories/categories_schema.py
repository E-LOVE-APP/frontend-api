from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic Categories pydantic schema"""


class CategoryBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the category in UUID format")
    category_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Name of the category"
    )

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    category_name: str = Field(..., max_length=50, min_length=1, description="Name of the category")
    category_descr: str = Field(
        ..., max_length=250, min_length=1, description="Descr of the category"
    )
    category_icon: str = Field(..., max_length=50, min_length=1, description="Icon of the category")


class CategoryUpdateSchema(CategoryBase):
    category_name: str = Field(..., max_length=50, min_length=1, description="Name of the category")
    category_descr: str = Field(
        ..., max_length=250, min_length=1, description="Descr of the category"
    )
    category_icon: str = Field(..., max_length=50, min_length=1, description="Icon of the category")


class CategoryOutput(CategoryBase):
    category_name: str = Field(..., max_length=50, min_length=1, description="Name of the category")
    category_descr: str = Field(
        ..., max_length=250, min_length=1, description="Descr of the category"
    )
    category_icon: str = Field(..., max_length=50, min_length=1, description="Icon of the category")


class CategoryListResponse(CategoryBase):
    categories: List[CategoryOutput]
