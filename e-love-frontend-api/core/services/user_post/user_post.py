import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.posts.user_post import UserPost
from core.schemas.posts.user_post_schema import PostCreate
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler
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
        self.paginator = Paginator[UserPost](db_session=db_session, model=UserPost)

    async def create_post(self, post_data: Dict[str, Any]) -> UserPost:
        return await self.create_object(
            model=UserPost,
            data=post_data,
        )

    async def get_post_by_id(self, post_id: UUID) -> UserPost:
        return await self.get_object_by_id(UserPost, post_id)

    async def get_post_list(
        self,
        limit: int = 10,
        next_token: Optional[str] = None,
    ) -> List[UserPost]:
        try:

            filters = None
            base_query = select(UserPost)

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
            logger.error(f"Error getting posts list: {e}")
            ExceptionHandler(e)

    async def update_post(self, post_id: UUID, update_data: UserPost) -> UserPost:
        """
        Обновляет информацию о посте пользователя.

        :param post_id: Идентификатор поста.
        :param update_data: Объект с обновленными данными поста.
        :return: Обновленный объект поста.
        :raises HTTPException: Возникает ошибка целостности данных или ошибка сервера.
        """
        try:
            return await self.update_object(
                model=UserPost, object_id=post_id, data=update_data.dict(exclude_unset=True)
            )
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating post {post_id}: {e}")
            ExceptionHandler(e)

    async def delete_post(self, post_id: UUID) -> None:
        try:
            await self.delete_object_by_id(UserPost, post_id)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting post {post_id}: {e}")
            ExceptionHandler(e)
