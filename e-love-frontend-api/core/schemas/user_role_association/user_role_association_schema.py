from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

"""Pydantic схемы для ассоциации ролей пользователя."""


class AddRoleToUserRequest(BaseModel):
    """
    Схема для добавления роли пользователю.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        role_id (UUID): UUID роли.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    role_id: UUID = Field(..., description="UUID of the role")


class AddRolesToUserRequest(BaseModel):
    """
    Схема для добавления нескольких ролей пользователю.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        role_ids (List[UUID]): Список UUID ролей для добавления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    role_ids: List[UUID] = Field(..., description="List of UUIDs of the roles to add")


class UpdateUserRolesRequest(BaseModel):
    """
    Схема для обновления ролей пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        new_role_ids (List[UUID]): Список новых UUID ролей для назначения пользователю.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    new_role_ids: List[UUID] = Field(
        ..., description="List of new role UUIDs to assign to the user"
    )


class RemoveRoleFromUserRequest(BaseModel):
    """
    Схема для удаления роли у пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        role_id (UUID): UUID роли для удаления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    role_id: UUID = Field(..., description="UUID of the role to remove")


class RemoveRolesFromUserRequest(BaseModel):
    """
    Схема для удаления нескольких ролей у пользователя.

    Атрибуты:
        user_id (UUID): UUID пользователя.
        role_ids (List[UUID]): Список UUID ролей для удаления.
    """

    user_id: UUID = Field(..., description="UUID of the user")
    role_ids: List[UUID] = Field(..., description="List of UUIDs of the roles to remove")
