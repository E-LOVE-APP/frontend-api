from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict

from core.schemas.users_categories.users_categories_schema import CategoryOutput
from core.schemas.posts.user_post_schema import PostOutput
from core.schemas.user_gender.user_gender_schema import UserGenderOutput
from core.db.models.posts.user_post import UserPost

"""Pydantic схемы для пользователей."""


class UserBase(BaseModel):
    """
    Базовая модель пользователя с общими полями.

    Атрибуты:
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        email (EmailStr): Уникальный email пользователя.
    """

    first_name: str = Field(..., max_length=50, min_length=1, description="First name of the user")
    last_name: str = Field(..., max_length=50, min_length=1, description="Last name of the user")
    email: EmailStr = Field(..., description="Unique email address of the user")

    model_config = ConfigDict(extra="forbid")


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.

    Атрибуты:
        password (str): Пароль пользователя.
    """

    password: str = Field(..., min_length=6, description="Password for the user")

    model_config = ConfigDict(extra="forbid")


class UserUpdate(BaseModel):
    """
    Схема для обновления существующего пользователя.

    Атрибуты:
        first_name (Optional[str]): Имя пользователя.
        last_name (Optional[str]): Фамилия пользователя.
        email (Optional[EmailStr]): Уникальный email пользователя.
        password (Optional[str]): Пароль пользователя.
    """

    first_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Last name of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Unique email address of the user")
    password: Optional[str] = Field(None, min_length=6, description="Password for the user")

    model_config = ConfigDict(extra="forbid")


class UserOutput(UserBase):
    """
    Схема для отображения данных пользователя.

    Атрибуты:
        id (UUID): ID пользователя в формате UUID.
        user_descr (Optional[str]): Описание пользователя.
        categories (Optional[List[CategoryOutput]]): Список категорий пользователя.
        posts (Optional[List[PostOutput]]): Список постов пользователя.
    """

    id: UUID = Field(..., description="ID of the user in UUID format")
    user_descr: Optional[str] = Field(None, max_length=500, description="Description of the user")
    gender: Optional[UserGenderOutput] = Field(None, description="User gender")
    categories: Optional[List[CategoryOutput]] = Field(
        None, description="List of user's categories"
    )
    posts: Optional[List[PostOutput]] = Field(None, description="List of user's posts")

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    # WHY? Проблема: Без явного преобразования Pydantic не знает, как преобразовать каждый UserPost в PostOutput (тут получаем список), и мы получаем ошибку валидации.
    # Однако, я не понимаю почему, но на categories это не распространяеться... Возможно проблема кроется просто в наличии from_attrs. Но я на всякий случай так же добавил и валидатор.
    # v - элемент pydantic. Если обнаружился объект типа UserPost - модели (alembic) - идет его преобразование (сериализация) в Pydantic-модель через from_orm стандартный метод.
    @validator("posts", pre=True, each_item=True)
    def convert_posts(cls, v):
        """
        Конвертирует ORM-объекты UserPost в Pydantic-модели PostOutput.

        Args:
            v: Значение элемента списка posts.

        Returns:
            PostOutput: Pydantic-модель поста.
        """
        if isinstance(v, UserPost):
            return PostOutput.from_orm(v)
        return v


class UsersListResponse(BaseModel):
    """
    Схема списка пользователей с информацией о пагинации.

    Атрибуты:
        users (List[UserOutput]): Список пользователей.
        has_next (bool): Индикатор наличия следующей страницы.
        next_token (Optional[str]): Токен для следующей страницы результатов.
    """

    users: List[UserOutput] = Field(..., description="List of users")
    has_next: bool = Field(..., description="Indicates if there is a next page")
    next_token: Optional[str] = Field(None, description="Token for the next page of results")

    model_config = ConfigDict(extra="forbid")


class UsersMatchingListResponse(BaseModel):
    """
    Схема ответа для списка подходящих пользователей.

    Атрибуты:
        matching_users (List[UserOutput]): Список подходящих пользователей.
        total (int): Общее количество подходящих пользователей.
        next_token (Optional[str]): Токен для следующей страницы результатов.
    """

    matching_users: List[UserOutput] = Field(..., description="List of matching users")
    total: int = Field(..., description="Total number of matching users")
    next_token: Optional[str] = Field(None, description="Token for the next page of results")

    model_config = ConfigDict(extra="forbid")
