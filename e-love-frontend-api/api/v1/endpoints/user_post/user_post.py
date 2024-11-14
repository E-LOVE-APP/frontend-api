from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.posts.user_post_schema import PostCreate, PostOutput, PostUpdate, PostsListResponse
from core.services.user_post.user_post import UserPostService

router = APIRouter(
    prefix="/user-post",
)


@router.post(
    "/",
    response_model=PostOutput,
    responses={
        200: {
            "description": "Create user post.",
            "model": PostOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User post", "Create user post"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
    ],
)
async def create_post(
    user_post_data: PostCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new user post.

    - **post_name**: Name of the user post

    """
    user_post_service = UserPostService(db)
    return await user_post_service.create_post(user_post_data.dict())


@router.get(
    "/{post_id}",
    response_model=PostOutput,
    responses={
        200: {
            "description": "Get the user post by id.",
            "model": PostOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User post", "Get user post"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_post_by_id(
    post_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a user post by it's ID.

    - **gener_id**: UUID of the user post
    """
    user_post_service = UserPostService(db)
    return await user_post_service.get_post_by_id(post_id)


@router.get(
    "/",
    response_model=PostsListResponse,
    responses={
        200: {
            "description": "Get user posts list.",
            "model": PostsListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User posts", "Get user posts list", "List"],
)
async def get_post_list(
    limit: int = Query(10, ge=1),
    next_token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
):
    user_post_service = UserPostService(db)
    response = await user_post_service.get_post_list(
        limit=limit,
        next_token=next_token,
    )
    return {
    "items": response["posts"],
    "has_next": response["has_next"],
    "next_token": response["next_token"],
}


@router.put(
    "/{post_id}",
    response_model=PostOutput,
    responses={
        200: {
            "description": "Update the user post by id.",
            "model": PostOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users post", "Update user post"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a user post information.

    - **post_id**: UUID of the user post
    - **post_update**: Fields to update
    """
    user_post_service = UserPostService(db)
    return await user_post_service.update_post(post_id, post_update)


@router.delete(
    "/{post_id}",
    responses={
        200: {
            "description": "Delete the user post by id.",
        },
        204: {
            "description": "There is no post with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["User post", "Delete user post"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a user post.

    - **post_id**: UUID of the user post
    """

    user_post_service = UserPostService(db)
    await user_post_service.delete_post(post_id)
    return {"message": "User post has been deleted successfully"}
