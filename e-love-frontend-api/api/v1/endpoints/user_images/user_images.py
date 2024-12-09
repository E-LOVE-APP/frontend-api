from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_images.user_images_schema import (
    UserImagesCreate,
    UserImagesListResponse,
    UserImagesOutput,
    UserImagesUpdate,
)
from core.services.user_images.user_images import UserImageService

router = APIRouter(
    prefix="/user-images",
)


@router.post(
    "/",
    response_model=UserImagesOutput,
    responses={
        200: {
            "description": "Create user image.",
            "model": UserImagesOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User image", "Create user image"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def create_image(
    user_image_data: UserImagesCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user image.

    - **image_name**: Name of the user image

    """
    user_image_service = UserImageService(db)
    data_dict = user_image_data.dict(exclude_unset=True)
    return await user_image_service.create_image(data_dict)


@router.get(
    "/{image_id}",
    response_model=UserImagesOutput,
    responses={
        200: {
            "description": "Get the user image by id.",
            "model": UserImagesOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User image", "Get user image"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_image_by_id(
    image_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user image by it's ID.

    - **gener_id**: UUID of the user image
    """
    user_image_service = UserImageService(db)
    return await user_image_service.get_image_by_id(image_id)


@router.get(
    "/",
    response_model=UserImagesListResponse,
    responses={
        200: {
            "description": "Get user images list.",
            "model": UserImagesListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User images", "Get user images list", "List"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_images_list(
    limit: int = 10,
    next_token: Optional[str] = None,
    db: AsyncSession = Depends(get_db_session),
):

    user_image_service = UserImageService(db)
    return await user_image_service.get_images_list(limit=limit, next_token=next_token)


@router.get(
    "/user/{user_id}",
    response_model=List[UserImagesOutput],
    responses={
        200: {
            "description": "Get all user images by user ID.",
            "model": List[UserImagesOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User images", "Get user images by user ID"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
    ],
)
async def get_user_images_list(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get all user images for a specific user ID.

    - **user_id**: UUID of the user
    """
    user_image_service = UserImageService(db)
    images = await user_image_service.get_user_images_list(user_id)
    return images


@router.put(
    "/{image_id}",
    response_model=UserImagesOutput,
    responses={
        200: {
            "description": "Update the user image by id.",
            "model": UserImagesOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users image", "Update user image"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_image(
    image_id: UUID,
    image_update: UserImagesUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user image information.

    - **image_id**: UUID of the user image
    - **image_update**: Fields to update
    """
    user_image_service = UserImageService(db)
    return await user_image_service.update_image(image_id, image_update)


@router.delete(
    "/{image_id}",
    responses={
        200: {
            "description": "Delete the user image by id.",
        },
        204: {
            "description": "There is no image with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User image", "Delete user image"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user image.

    - **image_id**: UUID of the user image
    """

    user_image_service = UserImageService(db)
    await user_image_service.delete_image(image_id)
    return {"message": "User image has been deleted successfully"}
