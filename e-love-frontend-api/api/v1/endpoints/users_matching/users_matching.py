# api/v1/endpoints/users_matching/users_matching.py

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import authenticator
from configuration.database import get_db_session
from core.db.models.users.users import User
from core.schemas.errors.httperror import HTTPError
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
    tags=["Users", "Get user list", "List", "AI", "Paginator", "Ai service"],
    dependencies=[
        Depends(authenticator.authenticate),
        validate_query_params(
            expected_params={"current_user_id", "limit", "next_token", "matching_type"}
        ),
    ],
)
async def get_matching_users_list(
    current_user_id: UUID,
    limit: int = 10,
    next_token: Optional[str] = None,
    matching_type: MatchingType = MatchingType.STANDARD,
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
        user_interaction_service=user_interaction_service,
        user_categories_service=user_categories_service,
    )

    matching_users, total, next_token = await users_matching_service.get_matching_users_list(
        current_user_id=current_user_id,
        limit=limit,
        matching_type=matching_type,
        next_token=next_token,
    )

    if matching_type != MatchingType.MAGIC:

        # Конвертируем пользователей в Pydantic модели. Оно конвертирует таким образом, что позволяет одновременно
        # иметь в выводе как UserOutput, так и CategoryOutput. Код не самый красивый, но я его позже подправлю
        # Сначала этот код отрезает лишние атрибуты из модели UserOutput, которые не входят в pydantic-схему
        # Потом туда добавляются CategoryOutput сущности категорий.
        # TODO: refactor

        matching_users_output = [UserOutput.from_orm(user) for user in matching_users]

        return UsersMatchingListResponse(
            matching_users=matching_users_output, total=total, next_token=next_token
        )
    else:
        return matching_users
