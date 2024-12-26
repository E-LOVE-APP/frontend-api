""" User service module """

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.users import User
from core.schemas.users.user_schema import UserUpdate
from core.services.base_service import BaseService
from exceptions.exception_handler import ExceptionHandler
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

    async def get_user_by_supabase_id(self, supabase_user_id: str) -> User:
        """
        Получает пользователя по supabase_user_id.

        :param supabase_user_id: Идентификатор пользователя в Supabase.
        :return: Объект пользователя.
        :raises HTTPException: Если пользователь не найден.
        """
        try:
            user = (
                (
                    await self.db_session.execute(
                        select(User).where(User.supabase_user_id == supabase_user_id)
                    )
                )
                .scalars()
                .first()
            )

            if not user:
                raise ExceptionHandler(
                    status_code=404,
                    detail="User with this supabase-id not found",
                )

            return user

        except Exception as e:
            logger.error(f"Error while fetching user by supabase_user_id: {e}")
            ExceptionHandler(e)

    # TODO: можно отрефакторить, если в user_data заместо any добавить доп. тип в виде словаря (модели юзера) для лучшей типизации
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        return await self.create_object(
            model=User,
            data=user_data,
            unique_fields=["email"],
            preprocess_func=self._preprocess_user,
        )

    async def create_user_after_sign_up(self, sub: str, payload_data: Dict[str, Any]) -> User:
        """
        Этот эндпоинт вызывается после signUp в Supabase.
        Создает пользователя в базе данных.

        params:
            sub: Идентификатор пользователя в Supabase.
            payload_data: Данные пользователя из Supabase.

        return: Объект пользователя.
        raises: HTTPException: Если пользователь не найден.
        """
        try:
            # Check if the user already exists in our database with the given sub (supabase_id)
            existing_user = self.get_user_by_supabase_id(sub)
            if existing_user:
                return existing_user
            else:
                user_data = {
                    "supabase_user_id": sub,
                    "email": payload_data["email"],
                    "first_name": payload_data["first_name"],
                    "last_name": payload_data["last_name"],
                    "status_id": payload_data.get("status_id"),
                    "roles": payload_data.get("roles"),
                }
                return await self.create_user(user_data)
                # TODO: assign user roles using user_roles_service

        except Exception as e:
            logger.error(f"Error while creating user after sign up")
            ExceptionHandler(e)

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

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error while fetching users: {e}")
            ExceptionHandler(e)

    async def update_user(self, user_id: UUID, update_data: UserUpdate) -> User:
        return await self.update_object(
            model=User,
            object_id=user_id,
            data=update_data.dict(exclude_unset=True),
            preprocess_func=self._preprocess_user,
        )

    async def delete_user(self, user_id: UUID) -> User:
        return await self.delete_object_by_id(User, user_id)

        # Если в других таблицах уже имеются записи про юзеров, мы не сможем удалить этого юзера, пока оттуда не будут удалены так же все его записи. Это Integrity error. Однако, я считаю достаточно целесообразно сделать возможным каскадно удалить все записи, связанные с юзером, при удалении самого юзера - потому-что если он сам хочет удалить аккаунт, или его банят, зачем после этого в БД тогда хранить его информацию? Возможно это не лучшая идея, это мы обсудить 12.10 на roadmap. TODO:
        # except Exception as e:
        #     await self.db_session.rollback()
        #     logger.error(f"Error while deleting user: {e}")
        #     ExceptionHandler(e)
