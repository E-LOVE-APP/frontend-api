""" Users matching service module """

import logging
from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Float, and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select, Subquery
from sqlalchemy.sql.elements import Label

from core.db.models.categories.categories import Categories
from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.users.users import User
from core.services.user_categories.user_categories import UserCategoriesAssociationService
from core.services.user_interaction.user_interaction import UserInteractionService
from exceptions.exception_handler import ExceptionHandler
from utils.custom_pagination import Paginator
from utils.enums.matching_type import MATCHING_PERCENTAGE_RANGES, MatchingType
from utils.functions.get_total_count import get_total_count

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UsersMatchingService:
    """
    Сервис для подбора пользователей на основе совпадения категорий.

    Этот сервис содержит методы для получения списка пользователей,
    которые совпадают по определенному проценту категорий с текущим пользователем.
    Он использует другие сервисы для получения данных о категориях пользователя и
    взаимодействиях с другими пользователями, а также предоставляет функциональность
    для построения и выполнения запросов к базе данных с использованием SQLAlchemy.
    """

    def __init__(
        self,
        db_session: AsyncSession,
        user_interaction_service: UserInteractionService,
        user_categories_service: UserCategoriesAssociationService,
    ):
        """
        Инициализирует экземпляр UsersMatchingService.

        Параметры:
            - db_session: Асинхронная сессия базы данных.
            - user_interaction_service: Сервис взаимодействий пользователей.
            - user_categories_service: Сервис категорий пользователей.
            - paginator: Кастомный пагинатор для результатов запроса.
        """
        self.db_session = db_session
        self.user_interaction_service = user_interaction_service
        self.user_categories_service = user_categories_service
        self.paginator = Paginator[User](db_session=db_session, model=User)

    async def build_potential_users_subquery(
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

    async def calculate_overlap_percentage(
        self, potential_users_subq: Subquery, num_curr_user_categories: int
    ) -> int:
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

    async def build_main_query(
        self,
        potential_users_subq: Subquery,
        overlap_percentage: Label,
        matching_type: MatchingType = MatchingType.STANDARD,
    ) -> Select:
        """
        Формирует основной запрос для получения пользователей с нужным процентом совпадения.

        Параметры:
            - potential_users_subq: Подзапрос с потенциальными пользователями.
            - overlap_percentage: Поле с процентом совпадения.
            - matching_type: Тип матчинга, по которому работает подбор юзеров. Влияет на процентовку.

        Возвращает:
            - Select: Основной запрос для выполнения.

        Описание:
            Этот метод строит основной запрос, который выбирает пользователей из таблицы `User`,
            соединяя их с подзапросом `potential_users_subq` по идентификатору пользователя.
            Затем применяет фильтр по проценту совпадения, выбирая пользователей с процентом
            совпадения от 20% до 40%. (в стандартном варианте)
            Результаты сортируются по убыванию процента совпадения.

        SQL-представление основного запроса:
            SELECT User.*
            FROM User
            JOIN potential_users_subq ON User.id = potential_users_subq.user_id
            WHERE overlap_percentage BETWEEN 20 AND 40
            ORDER BY overlap_percentage DESC;
        """
        min_percentage, max_percentage = MATCHING_PERCENTAGE_RANGES[matching_type]

        base_query = (
            select(User)
            .join(potential_users_subq, User.id == potential_users_subq.c.user_id)
            .where(and_(overlap_percentage >= min_percentage, overlap_percentage <= max_percentage))
            .order_by(overlap_percentage.desc())
        )

        return base_query

    # TODO: добавить так же вывод постов юзера
    async def get_matching_users_list(
        self,
        current_user_id: UUID,
        limit: int = 10,
        next_token: Optional[str] = None,
        matching_type: MatchingType = MatchingType.STANDARD,
    ) -> Tuple[List[User], int, Optional[str]]:
        """
        Возвращает список пользователей, соответствующих критериям совпадения по категориям.

        Параметры:
            - current_user_id: Идентификатор текущего пользователя.
            - limit: Количество пользователей для возврата (по умолчанию 10).
            - next_token: Токен для пагинации (по умолчанию None).
            - matching_type: Тип матчинга, определяющий диапазон процента совпадения.

        Возвращает:
            - Tuple[List[User], int, Optional[str]]: Список пользователей, соответствующих критериям.

        Исключения:
            - HTTPException: В случае ошибки базы данных или других проблем.

        Описание:
            Этот метод получает категории текущего пользователя, вычисляет потенциальных пользователей,
            с которыми есть общие категории, и вычисляет процент совпадения. Затем формирует основной
            запрос с учетом выбранного типа матчинга и возвращает результаты с применением пагинации.
        """
        try:
            curr_user_categories = await self.user_categories_service.get_user_categories(
                user_id=current_user_id
            )
            curr_user_categories_ids = [category.id for category in curr_user_categories]

            # TODO: переместить if-проверки?
            if not curr_user_categories_ids:
                return []

            viewed_users_ids = await self.user_interaction_service.get_viewed_users_list(
                current_user_id, paginate=False
            )

            # if not viewed_users_ids:
            #     return []

            potential_users_subquery = await self.build_potential_users_subquery(
                current_user_id=current_user_id,
                curr_user_category_ids=curr_user_categories_ids,
                viewed_users_ids=viewed_users_ids,
            )

            overlap_percentage_result = await self.calculate_overlap_percentage(
                potential_users_subq=potential_users_subquery,
                num_curr_user_categories=len(curr_user_categories_ids),
            )

            main_query = await self.build_main_query(
                potential_users_subq=potential_users_subquery,
                overlap_percentage=overlap_percentage_result,
                matching_type=matching_type,
            )

            paginated_response = await self.paginator.paginate_query(
                limit=limit,
                base_query=main_query,
                model_name="matching_users",
                next_token=next_token,
            )

            # Используем три строчки внизу для того чтобы вернуть Tuple в виде:
            # {matching_users: List[Users], total: len(matching_users), next_token: str}
            # TODO: этот функционал можно вынести в отдельную функцию, возможно даже в самом пагинаторе
            matching_users = paginated_response["matching_users"]
            total = await get_total_count(db_session=self.db_session, main_query=main_query)
            next_token = paginated_response["next_token"]

            return matching_users, total, next_token

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting users matching list: {e}")
            ExceptionHandler(e)
