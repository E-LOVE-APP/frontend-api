from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

"""Pydantic схемы для взаимодействий пользователей."""


class InteractionType(str, Enum):
    """Перечисление возможных типов взаимодействий."""

    MATCH = "MATCH"
    REJECT = "REJECT"


class UserInteractionBase(BaseModel):
    """
    Базовая модель взаимодействия пользователей с общими полями.

    Атрибуты:
        interaction_type (InteractionType): Тип взаимодействия (MATCH или REJECT).
        user_id (UUID): ID пользователя, инициировавшего взаимодействие.
        target_user_id (UUID): ID целевого пользователя.
    """

    interaction_type: InteractionType = Field(
        ..., description="Type of interaction (MATCH or REJECT)"
    )
    user_id: UUID = Field(..., description="ID of the current user that triggered the interaction")
    target_user_id: UUID = Field(
        ..., description="ID of the target user the interaction is aimed at"
    )

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserInteractionCreate(UserInteractionBase):
    """
    Схема для создания нового взаимодействия пользователей.
    """

    pass


class UserInteractionUpdate(BaseModel):
    """
    Схема для обновления существующего взаимодействия пользователей.

    Атрибуты:
        interaction_type (Optional[InteractionType]): Обновленный тип взаимодействия.
    """

    interaction_type: Optional[InteractionType] = Field(
        None, description="Updated type of interaction (MATCH or REJECT)"
    )

    model_config = ConfigDict(extra="forbid")


class UserInteractionOutput(UserInteractionBase):
    """
    Схема для отображения данных взаимодействия пользователей.

    Атрибуты:
        id (UUID): ID взаимодействия пользователей в формате UUID.
    """

    id: UUID = Field(..., description="ID of the user-interaction entity in UUID format")

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserInteractionsListResponse(BaseModel):
    """
    Схема для списка взаимодействий пользователей с информацией о пагинации.

    Атрибуты:
        user_interaction (List[UserInteractionOutput]): Список взаимодействий пользователей.
        has_next (bool): Индикатор наличия следующей страницы.
        next_token (Optional[str]): Токен для следующей страницы результатов.
    """

    user_interaction: List[UserInteractionOutput] = Field(
        ..., description="List of user interactions"
    )
    has_next: bool = Field(..., description="Indicates if there is a next page")
    next_token: Optional[str] = Field(None, description="Token for the next page of results")

    model_config = ConfigDict(extra="forbid")
