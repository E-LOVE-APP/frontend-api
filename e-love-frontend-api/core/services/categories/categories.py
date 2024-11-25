import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.categories.categories import Categories
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CategoriesService(BaseService):
    """Сервисный класс для управления категориями."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.paginator = Paginator[Categories](db_session=db_session, model=Categories)

    async def create_category(self, category_data: Dict[str, Any]) -> Categories:
        return await self.create_object(
            model=Categories, data=category_data, unique_fields=["category_name"]
        )

    async def get_category_by_id(self, category_id: UUID) -> Categories:
        return await self.get_object_by_id(Categories, category_id)

    async def get_categories_list(
        self,
        limit: int = 10,
        next_token: Optional[str] = None,
    ) -> List[Categories]:
        """
        Получает список категорий с пагинацией.

        :param limit: Количество категорий на странице (по умолчанию 10).
        :param next_token: Токен для получения следующей страницы.
        :return: Словарь с категориями и информацией о пагинации.
        """
        try:
            filters = None
            base_query = select(Categories)

            response = await self.paginator.paginate_query(
                base_query=base_query,
                next_token=next_token,
                filters=filters,
                model_name="items",
                limit=limit,
            )

            return response
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting categories list: {e}")
            ExceptionHandler(e)

    async def update_category(self, category_id: UUID, update_data: Dict[str, Any]) -> Categories:
        """
        Обновляет информацию о категории.

        :param category_id: Идентификатор категории.
        :param update_data: Объект с обновленными данными категории.
        :return: Обновленный объект категории.
        :raises HTTPException: Если возникает ошибка целостности данных или внутренняя ошибка сервера.
        """
        try:
            return await self.update_object(
                model=Categories, object_id=category_id, data=update_data
            )
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating category {category_id}: {e}")
            ExceptionHandler(e)

    async def delete_category(self, category_id: UUID) -> None:
        try:
            await self.delete_object_by_id(Categories, category_id)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting category {category_id}: {e}")
            ExceptionHandler(e)
