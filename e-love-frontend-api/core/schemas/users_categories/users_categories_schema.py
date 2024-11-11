# core/schemas/user_categories/user_categories_schema.py

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# TODO: add docstring!
class CategoryOutput(BaseModel):
    id: UUID
    category_name: str
    category_descr: str
    category_icon: Optional[str] = None

    class Config:
        orm_mode = True
        extra = "forbid"
        from_attributes = True
