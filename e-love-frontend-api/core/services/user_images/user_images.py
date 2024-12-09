""" User image service module """

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_images import UserImages
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserImageService(BaseService):
    """Сервисный класс для управления фотографиями пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserImageService.

        :param db_session: Асинхронная сессия базы данных.
        """
        self.paginator = Paginator[UserImages](db_session=db_session, model=UserImages)
        super().__init__(db_session)

    async def create_image(self, image_data: Dict[str, Any]) -> UserImages:
        """
        Создает новую фотографию в базе данных

        :param image_data: Словарь с данными о фотографии.
        :return: Созданный объект фотографии пользователя.
        """
        try:
            return await self.create_object(
                model=UserImages,
                data=image_data,
            )
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user image: {e}")
            ExceptionHandler(e)

    async def get_image_by_id(self, image_id: UUID) -> UserImages:
        """
        Получает фотографии пользователя по его ID.

        :param image_id: Идентификатор фотографии.
        :return: Объект фотографии пользователя.
        """
        try:
            return await self.get_object_by_id(UserImages, image_id)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting images: {e}")
            ExceptionHandler(e)

    async def get_images_list(
        self, limit: int = 10, next_token: Optional[str] = None
    ) -> List[UserImages]:
        try:
            base_query = select(UserImages)

            response = await self.paginator.paginate_query(
                base_query=base_query,
                next_token=next_token,
                model_name="items",
                limit=limit,
            )

            return response
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting posts list: {e}")
            ExceptionHandler(e)

    async def get_user_images_list(
        self, user_id: UUID, limit: int = 10, next_token: Optional[str] = None
    ) -> List[UserImages]:
        """
        Получить все изображения пользователя по user_id.

        :param user_id: Идентификатор пользователя.
        :return: Список изображений пользователя.
        """
        try:

            base_query = select(UserImages).where(UserImages.user_id == str(user_id))

            response = await self.paginator.paginate_query(
                base_query=base_query,
                next_token=next_token,
                model_name="items",
                limit=limit,
            )

            # Нужно получить список изображений из response
            items = response.get("items", [])
            return items
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting images list for user {user_id}: {e}")
            ExceptionHandler(e)

    async def update_image(self, image_id: UUID, update_data: Dict[str, Any]) -> UserImages:
        """
        Обновляет информацию о фотографию пользователя.

        :param image_id: Идентификатор фотографии.
        :param update_data: Словарь с данными  фотографий
        :return: Обновленный объект фотографии пользователя.
        """
        try:
            return await self.update_object(model=UserImages, object_id=image_id, data=update_data)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating post {image_id}: {e}")
            ExceptionHandler(e)

    async def delete_image(self, image_id: UUID) -> None:
        """
        Удаляет фотографию пользователя из базы данных.

        :param image_id: Идентификатор фотографии.
        """
        try:
            await self.delete_object_by_id(UserImages, image_id)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting image: {e}")
            ExceptionHandler(e)
