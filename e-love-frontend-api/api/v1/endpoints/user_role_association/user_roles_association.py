# api/v1/endpoints/user_role_association/user_role_association.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_role.user_role_schema import UserRoleOutput
from core.schemas.user_role_association.user_role_association_schema import (
    AddRolesToUserRequest,
    AddRoleToUserRequest,
    RemoveRoleFromUserRequest,
    RemoveRolesFromUserRequest,
    UpdateUserRolesRequest,
)
from core.schemas.users.user_schema import UserOutput
from core.services.user_role.user_role import UserRoleService
from core.services.user_roles.user_roles import UserRoleAssociationService
from core.services.users.users import UserService

router = APIRouter(prefix="/user-role-association", tags=["User Role Association"])


# Создаём зависимости для сервисов
def get_user_role_association_service(
    db: AsyncSession = Depends(get_db_session),
) -> UserRoleAssociationService:
    user_service = UserService(db)
    role_service = UserRoleService(db)
    return UserRoleAssociationService(db, user_service, role_service)


@router.post(
    "/add-role",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Role added to user successfully.",
            "content": {
                "application/json": {"example": {"message": "Role added to user successfully."}}
            },
        },
        400: {
            "description": "Bad Request.",
            "model": HTTPError,
        },
        404: {
            "description": "User or Role not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
    ],
)
async def add_role_to_user(
    request: AddRoleToUserRequest,
    service: UserRoleAssociationService = Depends(get_user_role_association_service),
):
    """
    Add a role to the user.

    - **user_id**: UUID of the user
    - **role_id**: UUID of the role to add
    """
    await service.add_role_to_user(request.user_id, request.role_id)
    return {"message": "Role added to user successfully."}


@router.post(
    "/add-roles",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Roles added to user successfully.",
            "content": {
                "application/json": {"example": {"message": "Roles added to user successfully."}}
            },
        },
        400: {
            "description": "Bad Request.",
            "model": HTTPError,
        },
        404: {
            "description": "User or one of the Roles not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
    ],
)
async def add_roles_to_user(
    request: AddRolesToUserRequest,
    service: UserRoleAssociationService = Depends(get_user_role_association_service),
):
    """
    Add multiple roles to a user.

    - **user_id**: UUID of the user
    - **role_ids**: List of UUIDs of roles to add
    """
    await service.add_roles_to_user(request.user_id, request.role_ids)
    return {"message": "Roles added to user successfully."}


@router.put(
    "/update-user-roles",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "User roles updated successfully.",
            "content": {
                "application/json": {"example": {"message": "User roles updated successfully."}}
            },
        },
        400: {
            "description": "Bad Request.",
            "model": HTTPError,
        },
        404: {
            "description": "User or one of the Roles not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def update_user_roles(
    request: UpdateUserRolesRequest,
    service: UserRoleAssociationService = Depends(get_user_role_association_service),
):
    """
    Update a user's roles by replacing existing roles with new ones.

    - **user_id**: UUID of the user
    - **new_role_ids**: List of new role UUIDs to assign to the user
    """
    await service.update_user_roles(request.user_id, request.new_role_ids)
    return {"message": "User roles updated successfully."}


@router.delete(
    "/remove-role",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Role removed from user successfully.",
            "content": {
                "application/json": {"example": {"message": "Role removed from user successfully."}}
            },
        },
        400: {
            "description": "Bad Request.",
            "model": HTTPError,
        },
        404: {
            "description": "User or Role not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def remove_role_from_user(
    request: RemoveRoleFromUserRequest,
    service: UserRoleAssociationService = Depends(get_user_role_association_service),
):
    """
    Remove a role from a user.

    - **user_id**: UUID of the user
    - **role_id**: UUID of the role to remove
    """
    await service.remove_role_from_user(request.user_id, request.role_id)
    return {"message": "Role removed from user successfully."}


@router.delete(
    "/remove-roles",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Roles removed from user successfully.",
            "content": {
                "application/json": {
                    "example": {"message": "Roles removed from user successfully."}
                }
            },
        },
        400: {
            "description": "Bad Request.",
            "model": HTTPError,
        },
        404: {
            "description": "User or one of the Roles not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def remove_roles_from_user(
    request: RemoveRolesFromUserRequest,
    service: UserRoleAssociationService = Depends(get_user_role_association_service),
):
    """
    Remove multiple roles from a user.

    - **user_id**: UUID of the user
    - **role_ids**: List of UUIDs of roles to remove
    """
    await service.remove_roles_from_user(request.user_id, request.role_ids)
    return {"message": "Roles removed from user successfully."}


@router.get(
    "/users-with-role/{role_id}",
    response_model=List[UserOutput],
    responses={
        200: {
            "description": "List of users with the specified role.",
            "model": List[UserOutput],
        },
        404: {
            "description": "Role not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User Role Association", "Get Users with Role"],
    dependencies=[
        Depends(get_db_session),
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def get_users_with_role(
    role_id: UUID, service: UserRoleAssociationService = Depends(get_user_role_association_service)
):
    """
    Get a list of users who have a specific role.

    - **role_id**: UUID of the role
    """
    users = await service.get_users_with_role(role_id)
    return users


@router.get(
    "/user-roles/{user_id}",
    response_model=List[UserRoleOutput],
    responses={
        200: {
            "description": "List of roles assigned to the specified user.",
            "model": List[UserRoleOutput],
        },
        404: {
            "description": "User not found.",
            "model": HTTPError,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User Role Association", "Get User Roles"],
    dependencies=[
        Depends(get_db_session),
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def get_user_roles(
    user_id: UUID, service: UserRoleAssociationService = Depends(get_user_role_association_service)
):
    """
    Get a list of roles assigned to a specific user.

    - **user_id**: UUID of the user
    """
    roles = await service.get_user_roles(user_id)
    return roles
