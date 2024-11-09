""" User interaction service module """

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_interaction import UserInteraction
from core.services.base_service import BaseService
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserInteractionService(BaseService):

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserInteractionService.

        :param db_session: Асинхронная сессия базы данных.
        :param paginator: ВАГИНАтор.
        """
        self.db_session = db_session
        self.paginator = Paginator[UserInteraction](db_session=db_session, model=UserInteraction)

    async def get_user_interaction_by_id(self, interaction_id: UUID) -> UserInteraction:
        return await self.get_object_by_id(UserInteraction, interaction_id)

    async def get_user_interactions_list(
        self,
        limit: int = 10,
        user_id: Optional[UUID] = None,
        target_user_id: Optional[UUID] = None,
        next_token: Optional[str] = None,
    ) -> List[UserInteraction]:
        """
        Получает список пользовательских вдаимодействий с другими пользователями (reject/match) с поддержкой пагинации.

        :param limit: Количество записей на странице.
        :param user_id: Фильтр по user_id (в данном случае имеется ввиду current_user_id).
        :return: Список объектов пользователей.
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            filters = None

            base_query = select(UserInteraction)

            if user_id:
                filters = UserInteraction.user_id == user_id

            if target_user_id:
                filters = UserInteraction.target_user_id == target_user_id

            response = await self.paginator.paginate_query(
                limit=limit,
                base_query=base_query,
                model_name="user_interaction",
                filters=filters,
                next_token=next_token,
            )

            return response

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while fetching user interactions list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    # WHY IDS:
    # Решено обойтись возвратом только списка id-шников просмотренных юзеров вместо полноценных объектов, для того чтобы
    # не добавлять лишних зависимостей. В бизнес-логике (матчинга) нету особой разницы.

    async def get_viewed_users_list(
        self,
        current_user_id: UUID,
        limit: int = 10,
        next_token: Optional[str] = None,
        paginate: bool = True,
    ) -> List[UUID]:
        """
        Получает список идентификаторов пользователей, с которыми текущий пользователь уже взаимодействовал.

        :param current_user_id: Идентификатор текущего пользователя.
        :param limit: Количество записей для пагинации.
        :param next_token: Токен для продолжения пагинации.
        :param paginate: Флаг, определяющий, применять ли пагинацию.
        :return: Список идентификаторов пользователей.
        """
        try:
            query = select(UserInteraction.target_user_id).where(
                UserInteraction.user_id == current_user_id
            )

            if paginate:
                response = await self.paginator.paginate_query(
                    limit=limit,
                    base_query=query,
                    model_name="user_interaction",
                    next_token=next_token,
                )
                viewed_users_ids = [item.target_user_id for item in response]
            else:
                result = await self.db_session.execute(query)
                viewed_users_ids = [row[0] for row in result.fetchall()]

            return viewed_users_ids

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Ошибка при получении списка просмотренных пользователей: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при получении списка просмотренных пользователей.",
            )

    # TODO: refactor - add the interaction type instead "Any"
    async def create_user_interaction(self, interaction_data: Dict[str, Any]) -> UserInteraction:
        return await self.create_object(model=UserInteraction, data=interaction_data)

    async def update_user_interaction(
        self, interaction_id: UUID, update_data: Dict[str, Any]
    ) -> UserInteraction:
        return await self.update_object(
            model=UserInteraction, object_id=interaction_id, data=update_data
        )

    async def delete_user_interaction(self, interaction_id: UUID) -> UserInteraction:
        try:
            return await self.delete_object_by_id(UserInteraction, interaction_id)

        # foreign key reference against another tables
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"IntegrityError while deleting the user interaction: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete the user interaction because it is referenced by other records.",
            )
