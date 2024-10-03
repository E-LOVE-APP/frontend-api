""" User service module """

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.models.users.users import User
from core.services.base_service import BaseService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserService(BaseService):
    """Сервисный класс для управления пользователями."""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализирует экземпляр UserService.

        :param db_session: Асинхронная сессия базы данных.
        """

        self.db_session = db_session

    # Пока что, временно используем dict, как входными данными. Я отдельно позже создам таску, где мы переделаем эти словари под DTO-objects.
    # Использование DTO будет намного лучше с точки зрения архитектуры.
    async def create_user(self, user_data: dict) -> User:
        """
        Создает нового пользователя.

        :param user_data: Словарь с данными пользователя.
        :return: Созданный объект пользователя.
        :raises HTTPException: Если email уже используется или произошла ошибка базы данных.
        """
        try:
            # Проверка, существует ли пользователь с таким email
            query = select(User).where(User.email == user_data["email"])
            result = await self.db_session.execute(query)
            user_exists = result.scalar_one_or_none()

            if user_exists:
                logger.warning(
                    f"Someone trying to create a user with existing email: {user_data['email']}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already taken by someone",
                )

            new_user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
            )

            new_user.set_password(user_data["password"])

            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)

            return new_user

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def get_user_by_id(self, user_id: UUID) -> User:
        """
        Получает пользователя по его ID.
        Использует унаследованный метод абстрактного класса BaseService.

        :param user_id: Идентификатор пользователя.
        :return: Объект пользователя.
        :raises HTTPException: Если пользователь не найден или произошла ошибка базы данных.
        """
        return await self.get_object_by_id(User, user_id)

    async def get_users_list(
        self, page: int = 1, size: int = 0, limit: int = 10, email: Optional[str] = None
    ) -> List[User]:
        """
        Получает список пользователей с поддержкой пагинации.

        :param page: Номер страницы (начиная с 1).
        :param size: Не используется (зарезервировано для будущего использования).
        :param limit: Количество записей на странице.
        :param email: Фильтр по email.
        :return: Список объектов пользователей.
        :raises HTTPException: Если произошла ошибка базы данных.
        """
        try:
            query = select(User).options(selectinload(User.roles))
            if email:
                query = query.where(User.email == email)
            query = query.offset((page - 1) * limit).limit(limit)

            result = await self.db_session.execute(query)
            users = result.scalars().all()
            return users

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while fetching users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_user(self, user_id: UUID, update_data: dict) -> User:
        """
        Обновляет информацию о пользователе.

        :param user_id: Идентификатор пользователя.
        :param update_data: Словарь с обновленными данными пользователя.
        :return: Обновленный объект пользователя.
        :raises HTTPException: Если пользователь не найден или произошла ошибка базы данных.
        """
        try:
            user = await self.get_user_by_id(user_id)

            if "password" in update_data:
                user.set_password(update_data.pop("password"))

            for key, value in update_data.items():
                setattr(user, key, value)

            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def delete_user(self, user_id: UUID) -> None:
        """
        Удаляет пользователя из базы данных.

        :param user_id: Идентификатор пользователя.
        :raises HTTPException: Если пользователь не найден или произошла ошибка базы данных.
        """
        try:
            user = await self.get_user_by_id(user_id)

            await self.db_session.delete(user)
            await self.db_session.commit()

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )
