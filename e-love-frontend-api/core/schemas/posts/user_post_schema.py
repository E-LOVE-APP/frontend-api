from typing import List, Optional

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

"""Pydantic схемы для постов пользователя."""


class PostBase(BaseModel):
    """
    Базовая модель поста с общими полями.

    Атрибуты:
        post_title (Optional[str]): Название поста.
    """

    post_title: Optional[str] = Field(
        None, max_length=250, min_length=1, description="Name of the post"
    )

    model_config = ConfigDict(extra="forbid")


class PostCreate(PostBase):
    """
    Схема для создания нового поста.

    Атрибуты:
        post_title (str): Название поста.
        post_descr (str): Описание поста.
        user_id (UUID): ID пользователя.
    """

    post_title: str = Field(..., max_length=250, min_length=1, description="Name of the post")
    post_descr: str = Field(
        ..., max_length=1000, min_length=1, description="Description of the post"
    )
    user_id: UUID = Field(..., description="ID of the user")

    model_config = ConfigDict(extra="forbid")


class PostUpdate(BaseModel):
    """
    Схема для обновления существующего поста.

    Атрибуты:
        post_title (Optional[str]): Название поста.
        post_descr (Optional[str]): Описание поста.
    """

    post_title: Optional[str] = Field(
        None, max_length=250, min_length=1, description="Name of the post"
    )
    post_descr: Optional[str] = Field(
        None, max_length=1000, min_length=1, description="Description of the post"
    )

    model_config = ConfigDict(extra="forbid")


class PostOutput(BaseModel):
    """
    Схема для отображения данных поста.

    Атрибуты:
        id (UUID): ID поста в формате UUID.
        post_title (str): Название поста.
        post_descr (str): Описание поста.
        user_id (UUID): ID пользователя.
        created_at (datetime): Дата и время создания.
        updated_at (Optional[datetime]): Дата и время последнего обновления.
    """

    id: UUID = Field(..., description="ID of the post in UUID format")
    post_title: str = Field(..., description="Name of the post")
    post_descr: str = Field(..., description="Description of the post")
    user_id: UUID = Field(..., description="ID of the user")
    created_at: datetime = Field(..., description="Creation date and time")
    updated_at: Optional[datetime] = Field(None, description="Last update date and time")

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class PostsListResponse(BaseModel):
    """
    Схема списка постов с информацией о пагинации.

    Атрибуты:
        items (List[PostOutput]): Список постов.
        has_next (bool): Индикатор наличия следующей страницы.
        next_token (Optional[str]): Токен для следующей страницы результатов.
    """

    items: List[PostOutput] = Field(..., description="List of posts")
    has_next: bool = Field(..., description="Indicates if there is a next page")
    next_token: Optional[str] = Field(None, description="Token for the next page of results")

    model_config = ConfigDict(extra="forbid")
