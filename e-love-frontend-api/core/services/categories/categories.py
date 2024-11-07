import logging
import uuid
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import asc, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.models.categories.categories import Categories
from core.services.base_service import BaseService
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CategoriesService(BaseService):
    """Сервисный класс для управления категориями."""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр CategoriesService.

        :param db_session: Асинхронная сессия базы данных.
        :param paginator: Пагинатор.
        """

        self.db_session = db_session
        self.paginator = Paginator[Category](db_session=db_session, model=Category)

        async def create_category(self, category_data: Dict[str, Any]) -> Category:
            return await self.create_object(
                model=Category, data=category_data, unique_fields=["category_name"]
            )

        async def get_category_by_id(self, category_id: UUID) -> Category:
            return await self.get_object_by_id(Category, category_id)

        async def get_category_list(self) -> List[Category]:
            try:
                query = select(Category)
                result = await self.db_session.execute(query)
                categories = result.scalars().all()
                return categories
            except SQLAlchemyError as e:
                await self.db_session.rollback()
                logger.error(f"Unexpected error while getting categories list: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected database error occurred",
                )

        async def update_category(self, category_id: UUID, update_data: Dict[str, Any]) -> Category:
            return await self.update_object(model=Category, object_id=category_id, data=update_data)

        async def delete_category(self, category_id: UUID) -> None:
            await self.delete_object_by_id(Category, category_id)
