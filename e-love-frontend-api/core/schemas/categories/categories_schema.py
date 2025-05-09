from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the category in UUID format")
    category_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Name of the category"
    )

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    category_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Name of the category"
    )
    category_descr: Optional[str] = Field(
        None, max_length=250, min_length=1, description="Descr of the role"
    )
    category_icon: Optional[str] = Field(
        None, max_length=250, min_length=1, description="icon of the role"
    )


class CategoryUpdateSchema(CategoryBase):
    category_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Name of the category"
    )
    category_descr: Optional[str] = Field(
        None, max_length=250, min_length=1, description="Descr of the role"
    )
    category_icon: Optional[str] = Field(
        None, max_length=250, min_length=1, description="icon of the role"
    )


class CategoryOutput(BaseModel):
    id: UUID
    category_name: str
    category_descr: str
    category_icon: Optional[str]

    class Config:
        orm_mode = True


class CategoriesListResponse(BaseModel):
    items: List[CategoryOutput]
    has_next: bool
    next_token: Optional[str]
