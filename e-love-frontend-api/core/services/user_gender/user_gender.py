""" User gender service module """

import logging
from typing import Any, Dict, List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_gender import UserGender
from core.services.base_service import BaseService

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
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            query = select(UserGender)
            result = await self.db_session.execute(query)
            genders = result.scalars().all()
            return genders
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting genders list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_gender(self, gender_id: UUID, update_data: Dict[str, Any]) -> UserGender:
        """
        Обновляет информацию о гендере пользователя.

        :param gender_id: Идентификатор гендера.
        :param update_data: Словарь с обновленными данными гендера.
        :return: Обновленный объект гендера пользователя.
        """
        try:
            updated_gender = await self.update_object(
                model=UserGender, object_id=gender_id, data=update_data
            )
            return updated_gender
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"Integrity error while updating gender {gender_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update gender due to related records in other tables."
            )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating gender {gender_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected database error occurred."
            )

    async def delete_gender(self, gender_id: UUID) -> None:
        """
        Удаляет гендер пользователя из базы данных.

        :param gender_id: Идентификатор роли.
        """
        await self.delete_object_by_id(UserGender, gender_id)
