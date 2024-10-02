""" User role service module """

import logging
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.user_role import UserRole

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserRoleService:
    """Сервисный класс для управления ролями пользователя"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user_role(self, role_data: dict) -> UserRole:
        try:
            # Проверка, существует ли роль с таким именем
            query = select(UserRole).where(UserRole.role_name == role_data["role_name"])
            result = await self.db_session.execute(query)
            role_exists = result.scalar_one_or_none()

            if role_exists:
                logger.warning(
                    f"Someone trying to create a user-role with existing role name: {role_data['role_name']}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This role is already exists",
                )

            new_role = UserRole(
                role_name=role_data["role_name"],
                # TODO: добавить сюда функционал текущего юзера, чтобы user_id брался из текущей сессии юзера. Пока не будет настроен JWT - этот метод использовать бессмысленно.
            )

            self.db_session.add(new_role)
            await self.db_session.commit()
            await self.db_session.refresh(new_role)

            return new_role

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def get_user_role_by_id(self, role_id: UUID) -> UserRole:
        """
        Получает роль пользователя по её ID.

        :param role_id: Идентификатор роли.
        :return: Объект роли пользователя.
        :raises HTTPException: Если роль не найдена или произошла ошибка базы данных.
        """
        try:
            query = select(UserRole).where(UserRole.id == role_id)
            result = await self.db_session.execute(query)
            role = result.scalar_one_or_none()
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")
            return role
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting user role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def get_user_roles_list(self) -> List[UserRole]:
        """
        Получает список всех ролей пользователей. На данный момент реализация пагинации тут будет излишней, поскольку самих ролей, которые существуют в соответствующей таблице БД < 10.

        :return: Список объектов ролей пользователей.
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            query = select(UserRole)
            result = await self.db_session.execute(query)
            roles = result.scalars().all()
            return roles
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while getting user roles list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_user_role(self, role_id: UUID, update_role_data: dict) -> UserRole:
        """
        Обновляет информацию о роли пользователя.

        :param role_id: Идентификатор роли.
        :param update_role_data: Словарь с обновленными данными роли.
        :return: Обновленный объект роли пользователя.
        :raises HTTPException: Если роль не найдена или произошла ошибка базы данных.
        """
        try:
            query = select(UserRole).where(UserRole.id == role_id)
            result = await self.db_session.execute(query)
            role = result.scalar_one_or_none()

            if not role:
                raise HTTPException(status_code=404, detail="Role not found")

            for key, value in update_role_data.items():
                setattr(role, key, value)

            await self.db_session.commit()
            await self.db_session.refresh(role)
            return role

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating this user role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def delete_user_role(self, role_id: UUID) -> None:
        """
        Удаляет роль пользователя из базы данных.

        :param role_id: Идентификатор роли.
        :raises HTTPException: Если роль не найдена или произошла ошибка базы данных.
        """
        try:
            query = select(UserRole).where(UserRole.id == role_id)
            result = await self.db_session.execute(query)
            role = result.scalar_one_or_none()

            if not role:
                raise HTTPException(status_code=404, detail="Role not found")

            await self.db_session.delete(role)
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting this user role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )
