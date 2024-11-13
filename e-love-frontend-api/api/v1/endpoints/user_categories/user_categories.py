from typing import List
from uuid import UUID

from auth.security import authenticator
from configuration.database import get_db_session
from core.schemas.categories.categories_schema import CategoryOutput
from core.schemas.errors.httperror import HTTPError
from core.schemas.user_categories_association.user_categories_association_schema import (
    AddCategoriesToUser,
    AddCategoryToUser,
    RemoveCategoriesFromUser,
    RemoveCategoryFromUser,
    UpdateUserCategories,
)
from core.schemas.users.user_schema import UserOutput
from core.services.categories.categories import CategoriesService
from core.services.user_categories.user_categories import (
    UserCategoriesAssociationService,
)
from core.services.users.users import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/user-categories",
    tags=["User Categories"],
)


@router.post(
    "/add",
    response_model=List[CategoryOutput],
    responses={
        200: {"description": "Category added to user successfully."},
        404: {"description": "User or category not found.", "model": HTTPError},
        500: {"description": "Server error.", "model": HTTPError},
    },
)
async def add_category_to_user(
    request: AddCategoryToUser,
    db_session: AsyncSession = Depends(get_db_session),
    _: UUID = Depends(authenticator.authenticate),
):
    user_service = UserService(db_session)
    category_service = CategoriesService(db_session)
    user_category_service = UserCategoriesAssociationService(
        db_session, user_service, category_service
    )
    try:
        await user_category_service.add_category_to_user(request.user_id, request.category_id)
        return {"message": "Category added to user successfully."}
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/add-multiple",
    responses={
        200: {"description": "Categories added to user successfully."},
        404: {"description": "User or categories not found.", "model": HTTPError},
        500: {"description": "Server error.", "model": HTTPError},
    },
)
async def add_categories_to_user(
    request: AddCategoriesToUser,
    db_session: AsyncSession = Depends(get_db_session),
    _: UUID = Depends(authenticator.authenticate),
):
    user_service = UserService(db_session)
    category_service = CategoriesService(db_session)
    user_category_service = UserCategoriesAssociationService(
        db_session, user_service, category_service
    )
    try:
        await user_category_service.add_categories_to_user(request.user_id, request.category_ids)
        return {"message": "Categories added to user successfully."}
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/update",
    responses={
        200: {"description": "User categories updated successfully."},
        404: {"description": "User or categories not found.", "model": HTTPError},
        500: {"description": "Server error.", "model": HTTPError},
    },
)
async def update_user_categories(
    request: UpdateUserCategories,
    db_session: AsyncSession = Depends(get_db_session),
    _: UUID = Depends(authenticator.authenticate),
):
    user_service = UserService(db_session)
    category_service = CategoriesService(db_session)
    user_category_service = UserCategoriesAssociationService(
        db_session, user_service, category_service
    )
    try:
        await user_category_service.update_user_categories(
            request.user_id, request.new_category_ids
        )
        return {"message": "User categories updated successfully."}
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/remove",
    responses={
        200: {"description": "Category removed from user successfully."},
        404: {"description": "User or category not found.", "model": HTTPError},
        500: {"description": "Server error.", "model": HTTPError},
    },
)
async def remove_category_from_user(
    request: RemoveCategoryFromUser,
    db_session: AsyncSession = Depends(get_db_session),
    _: UUID = Depends(authenticator.authenticate),
):
    user_service = UserService(db_session)
    category_service = CategoriesService(db_session)
    user_category_service = UserCategoriesAssociationService(
        db_session, user_service, category_service
    )
    try:
        await user_category_service.remove_category_from_user(request.user_id, request.category_id)
        return {"message": "Category removed from user successfully."}
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{user_id}",
    response_model=List[CategoryOutput],
    responses={
        200: {"description": "User categories retrieved successfully."},
        404: {"description": "User not found.", "model": HTTPError},
        500: {"description": "Server error.", "model": HTTPError},
    },
)
async def get_user_categories(
    user_id: UUID,
    db_session: AsyncSession = Depends(get_db_session),
    _: UUID = Depends(authenticator.authenticate),
):
    user_service = UserService(db_session)
    category_service = CategoriesService(db_session)
    user_category_service = UserCategoriesAssociationService(
        db_session, user_service, category_service
    )
    try:
        categories = await user_category_service.get_user_categories(user_id)
        return categories
    except HTTPException as e:
        raise e
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
