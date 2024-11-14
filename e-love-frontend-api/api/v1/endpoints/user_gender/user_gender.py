from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_gender.user_gender_schema import (
    UserGenderCreate,
    UserGenderOutput,
    UserGenderUpdate,
)
from core.services.user_gender.user_gender import UserGenderService

router = APIRouter(
    prefix="/user-gender",
)


@router.post(
    "/",
    response_model=UserGenderOutput,
    responses={
        200: {
            "description": "Create user gender.",
            "model": UserGenderOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User gender", "Create user gender"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def create_gender(
    gender_data: UserGenderCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user gender.

    - **gender_namee**: Name of the user gender

    """
    user_gender_service = UserGenderService(db)
    data_dict = gender_data.dict(exclude_unset=True)
    return await user_gender_service.create_gender(data_dict)


@router.get(
    "/{gender_id}",
    response_model=UserGenderOutput,
    responses={
        200: {
            "description": "Get the user gender by id.",
            "model": UserGenderOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User gender", "Get user gender"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_gender_by_id(
    gender_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user gender by it's ID.

    - **gener_id**: UUID of the user gender
    """
    user_gender_service = UserGenderService(db)
    return await user_gender_service.get_gender_by_id(gender_id)


@router.get(
    "/",
    response_model=List[UserGenderOutput],
    responses={
        200: {
            "description": "Get user genders list.",
            "model": List[UserGenderOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User genders", "Get user genders list", "List"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_genders_list(
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of user genders (without pagination, it's not needed here).

    """
    user_gender_service = UserGenderService(db)
    return await user_gender_service.get_genders_list()


@router.put(
    "/{gender_id}",
    response_model=UserGenderOutput,
    responses={
        200: {
            "description": "Update the user gender by id.",
            "model": UserGenderOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users gender", "Update user gender"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_gender(
    gender_id: UUID,
    gender_update: UserGenderUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user gender information.

    - **gender_id**: UUID of the user gender
    - **gender_update**: Fields to update
    """
    user_gender_service = UserGenderService(db)
    return await user_gender_service.update_gender(gender_id, gender_update)


@router.delete(
    "/{gender_id}",
    responses={
        200: {
            "description": "Delete the user gender by id.",
        },
        204: {
            "description": "There is no gender with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User gender", "Delete user gender"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_gender(
    gender_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user gender.

    - **gender_id**: UUID of the user gender
    """

    user_gender_service = UserGenderService(db)
    await user_gender_service.delete_gender(gender_id)
    return {"message": "User gender has been deleted successfully"}
