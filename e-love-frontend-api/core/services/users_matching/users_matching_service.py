""" Users matching service module """

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Float, and_, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Label, Select, Subquery

from core.db.models.categories.categories import Categories
from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.users.users import User
from core.services.user_categories.user_categories import UserCategoriesAssociationService
from core.services.user_interaction.user_interaction import UserInteractionService
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UsersMatchingService:
    """ """

    def __init__(
        self,
        db_session: AsyncSession,
        user_interaction_service: UserInteractionService,
        user_categories_service: UserCategoriesAssociationService,
        paginator: Paginator,
    ):
        self.db_session = db_session
        self.user_interaction_service = user_interaction_service
        self.user_categories_service = user_categories_service
        self.paginator = Paginator

    def build_potential_users_subquery(
        self,
        current_user_id: UUID,
        curr_user_category_ids: List[UUID],
        viewed_users_ids: List[UUID],
    ) -> Subquery:
        """
        Строит подзапрос для получения потенциальных пользователей и подсчета общих категорий.

        Параметры:
            - current_user_id: Идентификатор текущего пользователя.
            - curr_user_category_ids: Список идентификаторов категорий текущего пользователя.
            - viewed_users_ids: Список идентификаторов пользователей, с которыми уже было взаимодействие.

        Возвращает:
            - Subquery: Подзапрос для использования в основном запросе.

        Описание:
            Этот метод создает подзапрос, который выбирает пользователей, имеющих общие категории с текущим пользователем, исключая самого текущего пользователя и пользователей, с которыми уже было взаимодействие.
            Подсчитывается количество общих категорий для каждого потенциального пользователя.

        SQL-представление подзапроса:
            SELECT user_id, COUNT(category_id) AS common_category_count
            FROM user_categories
            WHERE category_id IN :curr_user_category_ids
              AND user_id != :current_user_id
              AND user_id NOT IN :viewed_users_ids
            GROUP BY user_id;
        """
        potential_users_subq = (
            select(
                user_categories_table.c.user_id.label("user_id"),
                func.count(user_categories_table.c.category_id).label("common_category_count"),
            )
            .where(
                and_(
                    user_categories_table.c.category_id.in_(curr_user_category_ids),
                    user_categories_table.c.user_id != current_user_id,
                    user_categories_table.c.user_id.not_in(viewed_users_ids),
                )
            )
            .group_by(user_categories_table.c.user_id)
        ).subquery()

        return potential_users_subq

    def calculate_overlap_percentage(
        self, potential_users_subq: Subquery, num_curr_user_categories: int
    ):
        """
        Вычисляет процент совпадения категорий для потенциальных пользователей.

        Параметры:
            - potential_users_subq: Подзапрос с потенциальными пользователями и количеством общих категорий.
            - num_curr_user_categories: Общее количество категорий текущего пользователя.

        Возвращает:
            - Label: Поле с вычисленным процентом совпадения для использования в запросе.

        Описание:
            Этот метод вычисляет процент совпадения категорий между текущим пользователем
            и потенциальными пользователями. Формула вычисления:
                overlap_percentage = (common_category_count / num_curr_user_categories) * 100

            Результат помечается как `overlap_percentage` для последующего использования
            в основном запросе.

        Пример вычисления:
            Если у текущего пользователя 5 категорий, а у потенциального пользователя
            2 общих категории, то:
                overlap_percentage = (2 / 5) * 100 = 40%
        """
        overlap_percentage = (
            (potential_users_subq.c.common_category_count.cast(Float) / num_curr_user_categories)
            * 100
        ).label("overlap_percentage")

        return overlap_percentage

    def build_main_query(self, potential_users_subq: Subquery, overlap_percentage: int):
        """
        Формирует основной запрос для получения пользователей с нужным процентом совпадения.

        Параметры:
            - potential_users_subq: Подзапрос с потенциальными пользователями.
            - overlap_percentage: Поле с процентом совпадения.

        Возвращает:
            - Select: Основной запрос для выполнения.

        Описание:
            Этот метод строит основной запрос, который выбирает пользователей из таблицы `User`,
            соединяя их с подзапросом `potential_users_subq` по идентификатору пользователя.
            Затем применяет фильтр по проценту совпадения, выбирая пользователей с процентом
            совпадения от 20% до 40%. Результаты сортируются по убыванию процента совпадения.

        SQL-представление основного запроса:
            SELECT User.*
            FROM User
            JOIN potential_users_subq ON User.id = potential_users_subq.user_id
            WHERE overlap_percentage BETWEEN 20 AND 40
            ORDER BY overlap_percentage DESC;
        """
        base_query = (
            select(User)
            .join(potential_users_subq, User.id == potential_users_subq.c.user_id)
            .where(and_(overlap_percentage >= 20, overlap_percentage <= 40))
            .order_by(overlap_percentage.desc())
        )

        return base_query

    async def get_matching_users_list(
        self,
        current_user_id: UUID,
        limit: int = 10,
        next_token: Optional[str] = None,
    ) -> List[User]:
        try:
            curr_user_categories = await self.user_categories_service.get_user_categories(
                current_user_id
            )

            curr_user_categories_ids = [category.id for category in curr_user_categories]

            if not curr_user_category_ids:
                return []

            viewed_users_ids = await self.user_interaction_service.get_viewed_users_list(
                current_user_id, paginate=False
            )

            main_query = self.build_main_query(
                self.build_potential_users_subquery(
                    current_user_id=current_user_id,
                    curr_user_category_ids=curr_user_categories_ids,
                    viewed_users_ids=viewed_users_ids,
                )
            )

            response = await self.paginator.paginate_query(
                limit=limit,
                base_query=main_query,
                model_name="matching_users",
                next_token=next_token,
            )

            return response

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Error while fetching matching users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching matching users.",
            )
