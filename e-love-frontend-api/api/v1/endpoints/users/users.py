# api/v1/endpoints/users/users.py

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.users.user_schema import UserCreate, UserOutput, UsersListResponse, UserUpdate
from core.services.users.users import UserService
from dependencies.validate_query_params import validate_query_params

router = APIRouter(
    prefix="/users",
)


@router.post(
    "/",
    response_model=UserOutput,
    responses={
        200: {
            "description": "Create user.",
            "model": UserOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Create user"],
    dependencies=[
        Depends(authenticator.authenticate),
        Depends(authenticator.require_role("Admin")),
    ],
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user.

    - **first_name**: First name of the user
    - **last_name**: Last name of the user
    - **email**: Email address of the user
    - **password**: Password for the user
    """
    user_service = UserService(db)
    return await user_service.create_user(user)


@router.get(
    "/{user_id}",
    response_model=UserOutput,
    responses={
        200: {
            "description": "Get the user by id.",
            "model": UserOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Get user"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user by their ID.

    - **user_id**: UUID of the user
    """
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)


@router.get(
    "/",
    response_model=UsersListResponse,
    responses={
        200: {
            "description": "Get users list. Support pagination",
            "model": UsersListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Get user list", "List"],
    dependencies=[
        Depends(authenticator.authenticate),
        validate_query_params(expected_params={"limit", "next_token", "email"}),
    ],
)
async def get_users_list(
    limit: int = 10,
    next_token: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of users with pagination.

    - **limit**: Number of users per page
    - **email**: Filter users by email
    """
    user_service = UserService(db)
    return await user_service.get_users_list(limit=limit, next_token=next_token, email=email)


@router.put(
    "/{user_id}",
    response_model=UserOutput,
    responses={
        200: {
            "description": "Update the user by id.",
            "model": UserOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Update user"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user's information.

    - **user_id**: UUID of the user
    - **user_update**: Fields to update
    """
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_update)


@router.delete(
    "/{user_id}",
    responses={
        200: {
            "description": "Delete the user by id.",
        },
        204: {
            "description": "There is no users with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Delete user"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user.

    - **user_id**: UUID of the user
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
