""" User gender service module """

import logging
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_gender import UserGender
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserGenderService(BaseService):
    """Сервисный класс для управления гендерами пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserGenderService.

        :param db_session: Асинхронная сесс��я базы данных.
        """
        super().__init__(db_session)

    async def create_gender(self, gender_data: Dict[str, Any]) -> UserGender:
        """
        Создает новый гендер.

        :param gender_data: Словарь с данными гендера.
        :return: Созданный объект гендера пользователя.
        """
        return await self.create_object(
            model=UserGender, data=gender_data, unique_fields=["gender_name"]
        )

    async def get_gender_by_id(self, gender_id: UUID) -> UserGender:
        """
        Получает гендер пользователя по его ID.

        :param gender_id: Идентификатор гендера.
        :return: Объект гендера пользователя.
        """
        return await self.get_object_by_id(UserGender, gender_id)

    async def get_genders_list(self) -> List[UserGender]:
        """
        Получает список гендеров

        :return: Список объектов ролей пользователей.
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            query = select(UserGender)
            result = await self.db_session.execute(query)
            genders = result.scalars().all()
            return genders
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting genders list: {e}")
            ExceptionHandler(e)

    async def update_gender(self, gender_id: UUID, update_data: Dict[str, Any]) -> UserGender:
        """
        Обновляет информацию о гендере пользователя.

        :param gender_id: Идентификатор гендера.
        :param update_data: Словарь с обновленными данными гендера.
        :return: Обновленный объект гендера пользователя.
        """
        try:
            return await self.update_object(model=UserGender, object_id=gender_id, data=update_data)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error updating genders list: {e}")
            ExceptionHandler(e)

    async def delete_gender(self, gender_id: UUID) -> None:
        """
        Удаляет гендер пользователя из базы данных.

        :param gender_id: Идентификатор роли.
        """
        try:
            await self.delete_object_by_id(UserGender, gender_id)
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error deleting genders list: {e}")
            ExceptionHandler(e)
