# api/v1/endpoints/users/users.py

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.users.user_schema import UserCreate, UserOutput, UserUpdateSchema
from core.services.users.users import UserService

router = APIRouter(
    prefix="/users",
)


# Пример корректного метода, с описанием для swagger; Тэги и responses можно будет отдельно создать в отдельных файлах, чтобы тут легко переиспользовать, чем я потом и займусь.
# POST-эндпоинт для юзера не подлежит реализации, пока не будет настроен Auth0.
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
    dependencies=[Depends(get_db_session)],
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
    return await user_service.create_user(user.dict())


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
    dependencies=[Depends(get_db_session)],
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
    response_model=List[UserOutput],
    responses={
        200: {
            "description": "Get users list. Support pagination",
            "model": List[UserOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Get user list", "List"],
    dependencies=[Depends(get_db_session)],
)
async def get_users_list(
    page: int = 1,
    limit: int = 10,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of users with pagination.

    - **page**: Page number (starting from 1)
    - **limit**: Number of users per page
    - **email**: Filter users by email
    """
    user_service = UserService(db)
    return await user_service.get_users_list(page=page, limit=limit, email=email)


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
    dependencies=[Depends(get_db_session)],
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdateSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user's information.

    - **user_id**: UUID of the user
    - **user_update**: Fields to update
    """
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_update.dict(exclude_unset=True))


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
    dependencies=[Depends(get_db_session)],
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
