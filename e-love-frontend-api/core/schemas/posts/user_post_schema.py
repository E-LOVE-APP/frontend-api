from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic Posts-model pydantic schema"""


class PostBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the post in UUID format")
    post_title: Optional[str] = Field(
        None, max_length=250, min_length=1, description="Name of the post"
    )

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    post_title: str = Field(..., max_length=250, min_length=1, description="Name of the post")
    post_descr: str = Field(..., max_length=1000, min_length=1, description="Descr of the post")
    user_id: UUID = Field(..., description="ID of the user")


class PostUpdate(PostBase):
    post_title: str = Field(..., max_length=250, min_length=1, description="Name of the post")
    post_descr: str = Field(..., max_length=1000, min_length=1, description="Descr of the post")


class PostOutput(PostBase):
    post_title: str = Field(..., max_length=250, min_length=1, description="Name of the post")
    post_descr: str = Field(..., max_length=1000, min_length=1, description="Descr of the post")


class PostsListResponse(BaseModel):
    posts: List[PostOutput]
