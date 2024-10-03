import logging
from uuid import UUID
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.users.users import UserService
from core.services.user_role.user_role import UserRoleService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserRoleAssociationService:
    """Сервис управления ролями пользователей."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_service = UserService(db_session)
        self.role_service = UserRoleService(db_session)

    async def add_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        """
        Добавляет роли пользователю.

        :param user_id: Идентификатор пользователя.
        :param role_id: Идентификатор роли.
        :raises HTTPException: Если пользователь или роли не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            role = await self.role_service.get_role_by_id(role_id)

            if role in user.roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has this role",
                )

            user.roles.append(role)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding role to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding role to the user.",
            )

    async def add_roles_to_user(self, user_id: UUID, role_ids: List[UUID]) -> None:
        """
        Добавляет > 1 роли пользователю. (BULK)

        :param user_id: Идентификатор пользователя.
        :param role_ids: Список идентификаторов ролей.
        :raises HTTPException: Если пользователь или роли не найдены, или произошла ошибка базы данных.
        """

        try:
            user = await self.user_service.get_user_by_id(user_id)
            roles_to_add = []
            for role_id in role_ids:
                role = await self.role_service.get_role_by_id(role_id)
                if role not in user.roles:
                    roles_to_add.append(role)

            if roles_to_add:
                user.roles.extend(roles_to_add)
                await self.db_session.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has this roles",
                )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding role to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding role to the user.",
            )

    async def update_user_roles(self, user_id: UUID, new_role_ids: List[UUID]) -> None:
        """
        Обновляет роли пользователя, заменяя существующие на новые.

        :param user_id: Идентификатор пользователя.
        :param new_role_ids: Список идентификаторов новых ролей.
        :raises HTTPException: Если пользователь или роли не найдены, или произошла ошибка базы данных.
        """
        try:
            # Уникальность
            new_role_ids = list(set(new_role_ids))

            user = await self.user_service.get_user_by_id(user_id)

            roles = []
            for role_id in new_role_ids:
                role = await self.role_service.get_role_by_id(role_id)
                roles.append(role)

            user.roles = roles
            await self.db_session.commit()

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while updating user roles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while updating user roles.",
            )

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """
        Удаляет роли пользователя.

        :param user_id: Идентификатор пользователя.
        :param role_id: Идентификатор роли.
        :raises HTTPException: Если пользователь или роли не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            role = await self.role_service.get_role_by_id(role_id)

            if role not in user.roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user doesn't have this role",
                )
            user.roles.remove(role)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while deleting role from the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while removing role from the user.",
            )

    async def remove_roles_from_user(self, user_id: UUID, role_ids: List[UUID]) -> None:
        """
        Удаляет > 1 ролей у пользователя. (BULK)

        :param user_id: Идентификатор пользователя.
        :param role_ids: Список идентификаторов ролей.
        :raises HTTPException: Если пользователь или роли не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            roles_to_remove = []

            for role_id in role_ids:
                role = await self.role_service.get_role_by_id(role_id)
                if role in user.roles:
                    roles_to_remove.append(role)

            if roles_to_remove:
                for role in roles_to_remove:
                    user.roles.remove(role)
                await self.db_session.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ни одна из указанных ролей не назначена пользователю.",
                )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while deleting roles from the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while removing roles from the user.",
            )

    async def get_users_with_role(self, role_id: UUID) -> List[User]:
        """
        Получает список пользователей, имеющих определенную роль.

        :param role_id: Идентификатор роли.
        :return: Список объектов User.
        :raises HTTPException: Если роль не найдена или произошла ошибка базы данных.
        """
        try:
            role = await self.role_service.get_role_by_id(role_id)
            return role.users
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while fetching users with role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while fetching users with role.",
            )
