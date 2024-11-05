""" User service module """

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
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
        :param paginator: Вагинатор.
        """

        self.db_session = db_session
        self.paginator = Paginator[User](db_session=db_session, model=User)

    async def _preprocess_user(self, user: User, data: Dict[str, Any]) -> None:
        password = data.pop("password", None)
        if password:
            user.set_password(password)

    # TODO: можно отрефакторить, если в user_data заместо any добавить доп. тип в виде словаря (модели юзера) для лучшей типизации
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        return await self.create_object(
            model=User,
            data=user_data,
            unique_fields=["email"],
            preprocess_func=self._preprocess_user,
        )

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self.get_object_by_id(User, user_id)

    async def get_users_list(
        self,
        limit: int = 10,
        email: Optional[str] = None,
        next_token: Optional[str] = None,
    ) -> List[User]:
        """
        Получает список пользователей с поддержкой пагинации.

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
        return await self.update_object(
            model=User,
            object_id=user_id,
            data=update_data.dict(exclude_unset=True),
            preprocess_func=self._preprocess_user,
        )

    async def delete_user(self, user_id: UUID) -> User:
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
