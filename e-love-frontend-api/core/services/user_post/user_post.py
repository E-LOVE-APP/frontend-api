import logging
from typing import Any, Dict, List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.posts.user_post import UserPost
from core.schemas.posts.user_post_schema import PostCreate
from core.services.base_service import BaseService
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserPostService(BaseService):
    """Сервисный класс для управления постами пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserPostService.

        :param db_session: Асинхронная сессия базы данных.
        :param paginator: Пагинатор.
        """

        super().__init__(db_session)

    async def create_post(self, post_data: UserPost) -> UserPost:
        # Чтобы создать объект необходимо преоброзовать модель в словарь
        post_data_dict = post_data.dict()
        return await self.create_object(
            model=UserPost,
            data=post_data_dict,
        )

    async def get_post_by_id(self, post_id: UUID) -> UserPost:
        return await self.get_object_by_id(UserPost, post_id)

    async def get_post_list(self) -> List[UserPost]:
        try:
            query = select(UserPost)
            result = await self.db_session.execute(query)
            posts = result.scalars().all()
            return posts
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting posts list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_post(self, post_id: UUID, update_data: UserPost) -> UserPost:
        return await self.update_object(
            model=UserPost, object_id=post_id, data=update_data.dict(exclude_unset=True)
        )

    async def delete_post(self, post_id: UUID) -> None:
        await self.delete_object_by_id(UserPost, post_id)
