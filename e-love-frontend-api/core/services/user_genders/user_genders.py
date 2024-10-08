import logging
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.users import User
from core.services.user_gender.user_gender import UserGenderService
from core.services.users.users import UserService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Пока что UserGenderService не реализован.
class UserGenderAssociationService:
    """Сервис управления гендерами пользователей."""

    def __init__(
        self, db_session: AsyncSession, user_service: UserService, gender_service: UserGenderService
    ):
        self.db_session = db_session
        self.user_service = user_service
        self.gender_service = gender_service

    async def add_gender_to_user(self, user_id: UUID, gender_id: UUID) -> None:
        """
        Добавляет гендер пользователю.

        :param user_id: Идентификатор пользователя.
        :param gender_id: Идентификатор гендера.
        :raises HTTPException: Если пользователь или гендер не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            gender = await self.gender_service.get_gender_by_id(gender_id)

            if gender in user.genders:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has this gender",
                )

            user.genders.append(gender)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding gender to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding gender to the user.",
            )

    async def add_genders_to_user(self, user_id: UUID, gender_ids: List[UUID]) -> None:
        """
        Добавляет несколько гендеров (>1) пользователю. (BULK)

        :param user_id: Идентификатор пользователя.
        :param gender_ids: Список идентификаторов гендеров.
        :raises HTTPException: Если пользователь или гендеры не найдены, или произошла ошибка базы данных.
        """

        try:
            user = await self.user_service.get_user_by_id(user_id)
            genders_to_add = []
            for gender_id in set(gender_ids):
                gender = await self.gender_service.get_gender_by_id(gender_id)
                if gender not in user.genders:
                    genders_to_add.append(gender)

            if genders_to_add:
                user.genders.extend(genders_to_add)
                await self.db_session.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has these genders",
                )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding genders to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding genders to the user.",
            )

    async def update_user_genders(self, user_id: UUID, new_gender_ids: List[UUID]) -> None:
        """
        Обновляет гендеры пользователя, заменяя существующие на новые. (>1)

        :param user_id: Идентификатор пользователя.
        :param new_gender_ids: Список идентификаторов новых гендеров.
        :raises HTTPException: Если пользователь или гендеры не найдены, или произошла ошибка базы данных.
        """
        try:
            new_gender_ids = list(set(new_gender_ids))
            user = await self.user_service.get_user_by_id(user_id)

            genders = []
            for gender_id in new_gender_ids:
                gender = await self.gender_service.get_gender_by_id(gender_id)
                genders.append(gender)

            user.genders = genders
            await self.db_session.commit()

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while updating user genders: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while updating user genders.",
            )

    async def remove_gender_from_user(self, user_id: UUID, gender_id: UUID) -> None:
        """
        Удаляет гендер у пользователя.

        :param user_id: Идентификатор пользователя.
        :param gender_id: Идентификатор гендера.
        :raises HTTPException: Если пользователь или гендер не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            gender = await self.gender_service.get_gender_by_id(gender_id)

            if gender not in user.genders:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user doesn't have this gender",
                )
            user.genders.remove(gender)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while removing gender from the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while removing gender from the user.",
            )

    async def remove_genders_from_user(self, user_id: UUID, gender_ids: List[UUID]) -> None:
        """
        Удаляет несколько гендеров (>1) у пользователя. (BULK)

        :param user_id: Идентификатор пользователя.
        :param gender_ids: Список идентификаторов гендеров.
        :raises HTTPException: Если пользователь или гендеры не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            genders_to_remove = []

            for gender_id in set(gender_ids):
                gender = await self.gender_service.get_gender_by_id(gender_id)
                if gender in user.genders:
                    genders_to_remove.append(gender)

            if genders_to_remove:
                for gender in genders_to_remove:
                    user.genders.remove(gender)
                await self.db_session.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="None of the specified genders are assigned to the user.",
                )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while removing genders from the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while removing genders from the user.",
            )

    async def get_users_with_gender(self, gender_id: UUID) -> List[User]:
        """
        Получает список пользователей, имеющих определенный гендер.

        :param gender_id: Идентификатор гендера.
        :return: Список объектов User.
        :raises HTTPException: Если гендер не найден или произошла ошибка базы данных.
        """
        try:
            gender = await self.gender_service.get_gender_by_id(gender_id)
            return gender.users
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while fetching users with gender: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while fetching users with gender.",
            )

    async def get_user_genders(self, user_id: UUID) -> List[UserGender]:
        """
        Получает список гендеров пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Список объектов UserGender.
        :raises HTTPException: Если пользователь не найден или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            return user.genders
        except SQLAlchemyError as e:
            logger.error(f"An error occurred while fetching genders of user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while fetching genders of user.",
            )
