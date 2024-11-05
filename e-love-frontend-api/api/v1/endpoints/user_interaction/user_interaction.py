# api/v1/endpoints/user_interaction/user_interaction.py

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError

# from core.schemas.users.user_schema import (
#     UserCreate,
#     UserOutput,
#     UsersListResponse,
#     UserUpdateSchema,
# )
from core.services.user_interaction.user_interaction import UserInteractionService
from dependencies.validate_query_params import validate_query_params

router = APIRouter(
    prefix="/user-interactions",
)


@router.post(
    "/",
    response_model=UserInteractionOutput,
    responses={
        200: {
            "description": "Create an user interaction.",
            "model": UserInteractionOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Create an user interaction", "User Interaction"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def create_user_interaction(
    user_interaction: UserInteractionCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user interaction.


    """
    user_interaction_service = UserInteractionService(db)
    return await user_interaction_service.create_user(user_interaction)


@router.get(
    "/{interaction_id}",
    response_model=UserInteractionOutput,
    responses={
        200: {
            "description": "Get an user interaction by id.",
            "model": UserInteractionOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Interactions", "Get user interaction"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def get_user_interaction_by_id(
    interaction_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user interaction by it's ID.

    - **interaction_id**: UUID of the user
    """
    user_interaction_service = UserInteractionService(db)
    return await user_interaction_service.get_user_interaction_by_id(interaction_id)


@router.get(
    "/",
    response_model=UserInteractionsListResponse,
    responses={
        200: {
            "description": "Get the user interactions list. Support pagination",
            "model": UserInteractionsListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Interactions", "Get user interactions list", "List"],
    dependencies=[
        Depends(authenticator.authenticate),
        validate_query_params(expected_params={"limit", "next_token", "user_id", "target_user_id"}),
    ],
)
async def get_user_interactions_list(
    limit: int = 10,
    next_token: Optional[str] = None,
    user_id: Optional[UUID] = None,
    target_user_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of user interactions with pagination.

    - **page**: Page number (starting from 1)
    - **limit**: Number of users per page
    # TODO: add correct comments
    """
    user_interaction_service = UserInteractionService(db)
    return await user_interaction_service.get_user_interactions_list(
        limit=limit, next_token=next_token, user_id=user_id, target_user_id=target_user_id
    )


@router.put(
    "/{interaction_id}",
    response_model=UserInteractionOutput,
    responses={
        200: {
            "description": "Update the user interaction by id.",
            "model": UserInteractionOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "User interaction", "Update an user interaction"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def update_user_interaction(
    interaction_id: UUID,
    update_data: UserInteractionUpdateSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user interaction information.

    - **user_id**: UUID of the user
    - **user_update**: Fields to update
    """
    user_interaction_service = UserInteractionService(db)
    return await user_interaction_service.update_user_interaction(user_id, update_data)


@router.delete(
    "/{interaction_id}",
    responses={
        200: {
            "description": "Delete the user interaction by id.",
        },
        204: {
            "description": "There is no user interactions with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "User interactions", "Delete the user interaction"],
    dependencies=[
        Depends(authenticator.authenticate),
    ],
)
async def delete_user_interaction(
    interaction_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user interaction.

    - **user_id**: UUID of the user
    """
    user_interaction_service = UserInteractionService(db)
    await user_interaction_service.delete_user_interaction(interaction_id)
    return {"message": "User interaction has been deleted successfully"}
