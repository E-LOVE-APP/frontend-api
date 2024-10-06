# core/schemas/user_role_association/user_role_association_schema.py

from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class AddRoleToUserRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    role_id: UUID = Field(..., description="UUID of the role")


class AddRolesToUserRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    role_ids: List[UUID] = Field(..., description="List of UUIDs of the roles to add")


class UpdateUserRolesRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    new_role_ids: List[UUID] = Field(
        ..., description="List of new role UUIDs to assign to the user"
    )


class RemoveRoleFromUserRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    role_id: UUID = Field(..., description="UUID of the role to remove")


class RemoveRolesFromUserRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    role_ids: List[UUID] = Field(..., description="List of UUIDs of the roles to remove")
