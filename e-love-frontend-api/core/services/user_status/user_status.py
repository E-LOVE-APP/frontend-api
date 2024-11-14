""" User status service module """

import logging
from typing import Any, Dict, List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_status import UserStatus
from core.services.base_service import BaseService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserStatusService(BaseService):
    """Сервисный класс для управления статусом пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserStatusService.

        :param db_session: Асинхронная сессия базы данных.
        """
        super().__init__(db_session)

    async def create_status(self, status_data: Dict[str, Any]) -> UserStatus:
        """
        Создает новый статус

        :param status_data: Словарь с данными статуса.
        :return: Созданный объект статуса пользователя.
        """
        return await self.create_object(
            model=UserStatus, data=status_data, unique_fields=["status_name"]
        )

    async def get_status_by_id(self, status_id: UUID) -> UserStatus:
        """
        Получает статус пользователя по его ID.

        :param status_id: Идентификатор статус.
        :return: Объект статуса пользователя.
        """
        return await self.get_object_by_id(UserStatus, status_id)

    async def get_status_list(self) -> List[UserStatus]:
        try:
            query = select(UserStatus)
            result = await self.db_session.execute(query)
            statuses = result.scalars().all()
            return statuses
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting status list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_status(self, status_id: UUID, update_data: Dict[str, Any]) -> UserStatus:
        """
        Обновляет информацию статусе пользователя.

        :param status_id: Идентификатор статуса.
        :param update_data: Словарь с обновленными данными статуса.
        :return: Обновленный объект статуса пользователя.
        """
        try:
            updated_status = await self.update_object(
                model=UserStatus, object_id=status_id, data=update_data
            )
            return updated_status
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"Integrity error while updating status {status_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update status due to related records in other tables."
            )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating status {status_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected database error occurred."
            )

    async def delete_status(self, status_id: UUID) -> None:
        """
        Удаляет статус пользователя из базы данных.

        :param status_id: Идентификатор роли.
        """
        await self.delete_object_by_id(UserStatus, status_id)
