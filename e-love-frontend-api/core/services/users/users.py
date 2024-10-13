""" User service module """

import logging
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import asc, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.models.users.users import User
from core.schemas.users.user_schema import UserUpdateSchema
from core.services.base_service import BaseService
from utils.custom_pagination import Paginator

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
        self.paginator = Paginator[User](db_session=db_session, model=User)

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
        try:
            return await self.get_object_by_id(User, user_id)
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while getting the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while getting the user.",
            )

    async def get_users_list(
        self,
        limit: int = 10,
        email: Optional[str] = None,
        next_token: Optional[str] = None,
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
            filters = None

            base_query = select(User)

            if email:
                filters = User.email == email

            response = await self.paginator.paginate_query(
                base_query=base_query,
                next_token=next_token,
                filters=filters,
                model_name="users",
                limit=limit,
            )

            return response

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while fetching users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def update_user(self, user_id: UUID, update_data: UserUpdateSchema) -> User:
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

        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"IntegrityError while updating the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update the user due to integrity constraints.",
            )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while updating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )

    async def delete_user(self, user_id: UUID) -> User:
        """
        Удаляет пользователя из базы данных.

        :param user_id: Идентификатор пользователя.
        :raises HTTPException: Если пользователь не найден или произошла ошибка базы данных.
        """
        try:
            return await self.delete_object_by_id(User, user_id)

        # Если в других таблицах уже имеются записи про юзеров, мы не сможем удалить этого юзера, пока оттуда не будут удалены так же все его записи. Это Integrity error. Однако, я считаю достаточно целесообразно сделать возможным каскадно удалить все записи, связанные с юзером, при удалении самого юзера - потому-что если он сам хочет удалить аккаунт, или его банят, зачем после этого в БД тогда хранить его информацию? Возможно это не лучшая идея, это мы обсудить 12.10 на roadmap. TODO:
        except IntegrityError as e:
            await self.db_session.rollback()
            logger.error(f"IntegrityError while deleting the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete the user because it is referenced by other records.",
            )

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while deleting user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred",
            )
