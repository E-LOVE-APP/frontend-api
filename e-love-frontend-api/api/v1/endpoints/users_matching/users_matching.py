# api/v1/endpoints/users_matching/users_matching.py

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import authenticator
from configuration.database import get_db_session
from core.db.models.users.users import User
from core.schemas.errors.httperror import HTTPError
from core.schemas.posts.user_post_schema import PostOutput
from core.schemas.users.user_schema import UserOutput, UsersListResponse, UsersMatchingListResponse
from core.schemas.users_categories.users_categories_schema import CategoryOutput
from core.services.categories.categories import CategoriesService
from core.services.user_categories.user_categories import UserCategoriesAssociationService
from core.services.user_interaction.user_interaction import UserInteractionService
from core.services.users.users import UserService
from core.services.users_matching.users_matching_service import UsersMatchingService
from dependencies.validate_query_params import validate_query_params
from utils.custom_pagination import Paginator
from utils.enums.matching_type import MatchingType

router = APIRouter(prefix="/users-matching")


@router.get(
    "/",
    response_model=UsersMatchingListResponse,
    responses={
        200: {
            "description": "Get matching-users list. Support pagination",
            "model": UsersMatchingListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users", "Get user list", "List"],
    dependencies=[
        Depends(authenticator.authenticate),
        validate_query_params(
            expected_params={
                "current_user_id",
                "limit",
                "next_token",
                "matching_type",
                "post_limit",
                "categories_limit",
            }
        ),
    ],
)
async def get_matching_users_list(
    current_user_id: UUID,
    limit: int = 10,
    next_token: Optional[str] = None,
    matching_type: MatchingType = MatchingType.STANDARD,
    post_limit: int = 5,
    categories_limit: int = 5,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a list of matching-users with pagination.

    - **current_user_id**: Id of the current user
    - **limit**: Number of users per page
    - **next_token**: Token to the next N user-entities
    - **matching_type**: Type of the matching
    """

    # REMARK: так лучше не делать
    # TODO: REFACTOR

    user_service = UserService(db_session=db)
    category_service = CategoriesService(db_session=db)
    user_interaction_service = UserInteractionService(db_session=db)

    user_categories_service = UserCategoriesAssociationService(
        db_session=db, user_service=user_service, category_service=category_service
    )

    users_matching_service = UsersMatchingService(
        db_session=db,
        user_interaction_service=UserInteractionService(db_session=db),
        user_categories_service=UserCategoriesAssociationService(
            db_session=db,
            user_service=UserService(db_session=db),
            category_service=CategoriesService(db_session=db),
        ),
    )

    matching_users, total, next_token = await users_matching_service.get_matching_users_list(
        current_user_id=current_user_id,
        limit=limit,
        matching_type=matching_type,
        next_token=next_token,
        post_limit=post_limit,
        categories_limit=categories_limit,
    )

    # Конвертируем пользователей в Pydantic модели. Оно конвертирует таким образом, что позволяет одновременно
    # иметь в выводе как UserOutput, так и CategoryOutput. Код не самый красивый, но я его позже подправлю
    # Сначала этот код отрезает лишние атрибуты из модели UserOutput, которые не входят в pydantic-схему
    # Потом туда добавляются CategoryOutput сущности категорий.
    # TODO: refactor
    matching_users_output = [
        UserOutput(**{k: v for k, v in user.__dict__.items() if k in UserOutput.__fields__})
        for user in matching_users
    ]

    """
    Преобразование ORM-моделей категорий и постов пользователя в Pydantic-схемы 
    для корректной сериализации и возврата в API-ответе
    """
    for i, user in enumerate(matching_users_output):
        user_categories = matching_users[i].categories
        user.categories = [
            CategoryOutput(
                id=category.id,
                category_name=category.category_name,
                category_descr=category.category_descr,
                category_icon=category.category_icon,
            )
            for category in user_categories
        ]
        user_posts = matching_users[i].posts
        user.posts = [
            PostOutput(
                id=post.id,
                post_title=post.post_title,
                post_descr=post.post_descr,
                user_id=post.user_id,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in user_posts
        ]

    return UsersMatchingListResponse(
        matching_users=matching_users_output, total=total, next_token=next_token
    )
