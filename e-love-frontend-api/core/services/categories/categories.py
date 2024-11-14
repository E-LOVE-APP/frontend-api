import logging
from typing import Any, Dict, List
from uuid import UUID

from core.db.models.categories.categories import Categories
from core.services.base_service import BaseService
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CategoriesService(BaseService):
    """Сервисный класс для управления категориями."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.db_session = db_session
        self.paginator = Paginator[Categories](db_session=db_session, model=Categories)

    async def create_category(self, category_data: Categories) -> Categories:
        # Чтобы создать объект необходимо преоброзовать модель в словарь
        category_data_dict = category_data.dict()
        return await self.create_object(
            model=Categories, data=category_data_dict, unique_fields=["category_name"]
        )

    async def get_category_by_id(self, category_id: UUID) -> Categories:
        return await self.get_object_by_id(Categories, category_id)

    async def get_category_list(self) -> List[Categories]:
        try:
            query = select(Categories)
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

    async def update_category(self, category_id: UUID, update_data: Categories) -> Categories:
        # Чтобы обновить объект необходимо преоброзовать модель в словарь
        return await self.update_object(
            model=Categories, object_id=category_id, data=update_data.dict(exclude_unset=True)
        )

    async def delete_category(self, category_id: UUID) -> None:
        await self.delete_object_by_id(Categories, category_id)
