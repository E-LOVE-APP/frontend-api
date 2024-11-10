from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import Authenticator, authenticator
from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.categories.categories_schema import (
    CategoryCreate,
    CategoryOutput,
    CategoryUpdateSchema,
)
from core.services.categories.categories import CategoriesService

router = APIRouter(
    prefix="/categories",
)


@router.post(
    "/",
    response_model=CategoryOutput,
    responses={
        200: {
            "description": "Create category.",
            "model": CategoryOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Categories", "Create a category"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new category.

    - **category_name**: Name of the category

    """
    categories_service = CategoriesService(db)
    return await categories_service.create_category(category_data)


@router.get(
    "/{category_id}",
    response_model=CategoryOutput,
    responses={
        200: {
            "description": "Get the category by id.",
            "model": CategoryOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Categories", "Get category"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_category_by_id(
    category_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a category by it's ID.

    - **gener_id**: UUID of the category
    """
    categories_service = CategoriesService(db)
    return await categories_service.get_category_by_id(category_id)


@router.get(
    "/",
    response_model=List[CategoryOutput],
    responses={
        200: {
            "description": "Get categories list.",
            "model": List[CategoryOutput],
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Categories", "Get categories list", "List"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_category_list(
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of categories.

    """
    categories_service = CategoriesService(db)
    return await categories_service.get_category_list()


@router.put(
    "/{category_id}",
    response_model=CategoryOutput,
    responses={
        200: {
            "description": "Update the category by id.",
            "model": CategoryOutput,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Categories", "Update category"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def update_category(
    category_id: UUID,
    category_update: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a category information.

    - **category_id**: UUID of the user category
    - **category_update**: Fields to update
    """
    categories_service = CategoriesService(db)
    return await categories_service.update_category(category_id, category_update)


@router.delete(
    "/{category_id}",
    responses={
        200: {
            "description": "Delete the category by id.",
        },
        204: {
            "description": "There is no category with provided id.",
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Categories", "Delete category"],
    dependencies=[
        Depends(get_db_session),
        Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a category.

    - **category_id**: UUID of the category
    """

    categories_service = CategoriesService(db)
    await categories_service.delete_category(category_id)
    return {"message": "Category has been deleted successfully"}
