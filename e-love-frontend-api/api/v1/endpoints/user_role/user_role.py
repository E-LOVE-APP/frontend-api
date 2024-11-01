# api/v1/endpoints/user_role/user_role.py

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_role.user_role_schema import UserRoleCreate, UserRoleOutput, UserRoleUpdate
from core.services.user_role.user_role import UserRoleService

router = APIRouter(
    prefix="/user-role",
)


@router.post(
    "/",
    response_model=UserRoleOutput,
    responses={
        200: {
            "description": "Create user role.",
            "model": UserRoleOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User role", "Create user role"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def create_user_role(
    user_role_data: UserRoleCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user role.

    - **role_namee**: Name of the user role

    """
    user_role_service = UserRoleService(db)
    return await user_role_service.create_user_role(user_role_data)


@router.get(
    "/{role_id}",
    response_model=UserRoleOutput,
    responses={
        200: {
            "description": "Get the user role by id.",
            "model": UserRoleOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User role", "Get user role"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_role_by_id(
    role_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user role by it's ID.

    - **role_id**: UUID of the user role
    """
    user_role_service = UserRoleService(db)
    return await user_role_service.get_role_by_id(role_id)


@router.get(
    "/",
    response_model=List[UserRoleOutput],
    responses={
        200: {
            "description": "Get user roles list.",
            "model": List[UserRoleOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User roles", "Get user roles list", "List"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_user_roles_list(
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of user roles (without pagination, it's not needed here).

    """
    user_role_service = UserRoleService(db)
    return await user_role_service.get_user_roles_list()


@router.put(
    "/{role_id}",
    response_model=UserRoleOutput,
    responses={
        200: {
            "description": "Update the user role by id.",
            "model": UserRoleOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users role", "Update user role"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_user_role(
    role_id: UUID,
    role_update: UserRoleUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user role information.

    - **role_id**: UUID of the user role
    - **role_update**: Fields to update
    """
    user_role_service = UserRoleService(db)
    return await user_role_service.update_user_role(role_id, role_update)


@router.delete(
    "/{role_id}",
    responses={
        200: {
            "description": "Delete the user role by id.",
        },
        204: {
            "description": "There is no role with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User role", "Delete user role"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_user_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user role.

    - **role_id**: UUID of the user role
    """

    user_role_service = UserRoleService(db)
    await user_role_service.delete_user_role(role_id)
    return {"message": "User role has been deleted successfully"}
