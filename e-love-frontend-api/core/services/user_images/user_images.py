""" User image service module """

import logging
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_images import UserImages
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserImageService(BaseService):
    """Сервисный класс для управления фотографиями пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserImageService.

        :param db_session: Асинхронная сессия базы данных.
        """
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

    async def get_images_list(self) -> List[UserImages]:
        try:
            query = select(UserImages)
            result = await self.db_session.execute(query)
            images = result.scalars().all()
            return images
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting images list: {e}")
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
            logger.error(f"Unexpected error while updating image: {e}")
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
