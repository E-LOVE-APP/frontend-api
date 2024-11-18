""" User role service module """

import logging
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_role import UserRole
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserRoleService(BaseService):
    """Сервисный класс для управления ролями пользователя"""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserRoleService.

        :param db_session: Асинхронная сессия базы данных.
        """
        super().__init__(db_session)

    async def create_user_role(self, role_data: Dict[str, Any]) -> UserRole:
        """
        Создает новую роль пользователя.

        :param role_data: Словарь с данными роли.
        :return: Созданный объект роли пользователя.
        """
        return await self.create_object(model=UserRole, data=role_data, unique_fields=["role_name"])

    async def get_role_by_id(self, role_id: UUID) -> UserRole:
        """
        Получает роль пользователя по её ID.

        :param role_id: Идентификатор роли.
        :return: Объект роли пользователя.
        """
        return await self.get_object_by_id(UserRole, role_id)

    async def get_user_roles_list(self) -> List[UserRole]:
        """
        Получает список всех ролей пользователей.

        :return: Список объектов ролей пользователей.
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            query = select(UserRole)
            result = await self.db_session.execute(query)
            roles = result.scalars().all()
            return roles
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error getting user roles list: {e}")
            ExceptionHandler(e)

    async def update_user_role(self, role_id: UUID, update_data: Dict[str, Any]) -> UserRole:
        """
        Обновляет информацию о роли пользователя.

        :param role_id: Идентификатор роли.
        :param update_data: Словарь с обновленными данными роли.
        :return: Обновленный объект роли пользователя.
        """
        return await self.update_object(model=UserRole, object_id=role_id, data=update_data)

    async def delete_user_role(self, role_id: UUID) -> None:
        """
        Удаляет роль пользователя из базы данных.

        :param role_id: Идентификатор роли.
        """
        await self.delete_object_by_id(UserRole, role_id)
