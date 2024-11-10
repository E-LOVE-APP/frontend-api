from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_status.user_status_schema import (
    UserStatusCreate,
    UserStatusUpdate,
    UserStatusOutput,
)
from core.services.user_status.user_status import UserStatusService

router = APIRouter(
    prefix="/user-status",
)


@router.post(
    "/",
    response_model=UserStatusOutput,
    responses={
        200: {
            "description": "Create user status.",
            "model": UserStatusOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User status", "Create user status"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def create_status(
    user_status_data: UserStatusCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user status.

    - **status_name**: Name of the user status

    """
    user_status_service = UserStatusService(db)
    return await user_status_service.create_status(user_status_data)


@router.get(
    "/{status_id}",
    response_model=UserStatusOutput,
    responses={
        200: {
            "description": "Get the user status by id.",
            "model": UserStatusOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User status", "Get user status"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_status_by_id(
    status_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user status by it's ID.

    - **gener_id**: UUID of the user status
    """
    user_status_service = UserStatusService(db)
    return await user_status_service.get_status_by_id(status_id)


@router.get(
    "/",
    response_model=List[UserStatusOutput],
    responses={
        200: {
            "description": "Get user statuses list.",
            "model": List[UserStatusOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User statuses", "Get user statuses list", "List"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_status_list(
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of user statuses (without pagination, it's not needed here).

    """
    user_status_service = UserStatusService(db)
    return await user_status_service.get_status_list()


@router.put(
    "/{status_id}",
    response_model=UserStatusOutput,
    responses={
        200: {
            "description": "Update the user status by id.",
            "model": UserStatusOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users status", "Update user status"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_status(
    status_id: UUID,
    status_update: UserStatusUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user status information.

    - **status_id**: UUID of the user status
    - **status_update**: Fields to update
    """
    user_status_service = UserStatusService(db)
    return await user_status_service.update_status(status_id, status_update)


@router.delete(
    "/{status_id}",
    responses={
        200: {
            "description": "Delete the user status by id.",
        },
        204: {
            "description": "There is no status with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User status", "Delete user status"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_status(
    status_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user status.

    - **status_id**: UUID of the user status
    """

    user_status_service = UserStatusService(db)
    await user_status_service.delete_status(status_id)
    return {"message": "User status has been deleted successfully"}
