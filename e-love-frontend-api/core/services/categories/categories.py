import logging
from typing import Any, Dict, List
from uuid import UUID

from core.db.models.categories.categories import Categories
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
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

    async def get_category_list(self) -> List[Categories]:
        try:
            query = select(Categories)
            result = await self.db_session.execute(query)
            categories = result.scalars().all()
            return categories
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting categories list: {e}")
            ExceptionHandler(e)

    async def update_category(self, category_id: UUID, update_data: Dict[str, Any]) -> Categories:
        return await self.update_object(model=Categories, object_id=category_id, data=update_data)

    async def delete_category(self, category_id: UUID) -> None:
        await self.delete_object_by_id(Categories, category_id)
