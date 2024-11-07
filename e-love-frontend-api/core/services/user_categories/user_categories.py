import logging
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.users.users import User
from core.db.models.categories.categories import Category
from core.services.categories.categories import CategoriesService
from core.services.users.users import UserService


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UserCategoriesAssociationService:
    """Сервис управления гендерами пользователей."""
    
    def __init__(
        self, db_session: AsyncSession, user_service: UserService, categories_service: CategoriesService
    ):
        self.db_session = db_session
        self.user_service = user_service
        self.category_service = category_service
        
    async def add_category_to_user(self, user_id: UUID, category_id: UUID) -> None:
        """
        Добавляет категорию пользователю.

        :param user_id: Идентификатор пользователя.
        :param category_id: Идентификатор гендера.
        :raises HTTPException: Если пользователь или катгеория не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            category = await self.category_service.get_category_by_id(category_id)

            if category in user.categories:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has this category",
                )

            user.categories.append(category)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding category to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding category to the user.",
            )
            
    
    async def add_categories_to_user(self, user_id: UUID, category_ids: List[UUID]) -> None:
         """
        Добавляет несколько категорий (>1) пользователю. (BULK)

        :param user_id: Идентификатор пользователя.
        :param category_ids: Список идентификаторов категорий.
        :raises HTTPException: Если пользователь или категории не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            categories_to_add = []
            for category_id in set(category_ids):
                category = await self.category_service.get_category_by_id(category_id)
                if category not in user.categories:
                    categories_to_add.append(category)

            if categories_to_add:
                user.categories.extend(categories_to_add)
                await self.db_session.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user already has these categories",
                )
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while adding categories to the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while adding categories to the user.",
            )
            
    async def update_user_categories(self, user_id: UUID, new_categories_ids: List[UUID]) -> None:
        """
        Обновляет категории пользователя, заменяя существующие на новые. (>1)

        :param user_id: Идентификатор пользователя.
        :param new_categories_ids: Список идентификаторов новых категорий.
        :raises HTTPException: Если пользователь или категории не найдены, или произошла ошибка базы данных.
        """
        try:
            new_categories_ids = list(set(new_categories_ids))
            user = await self.user_service.get_user_by_id(user_id)

            categories = []
            for category_id in new_categories_ids:
                category = await self.category_service.get_category_by_id(category_id)
                categories.append(category)

            user.categories = categories
            await self.db_session.commit()

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while updating user categories: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while updating user categories.",
            )
            
    async def remove_category_from_user(self, user_id: UUID, category_id: UUID) -> None:
        """
        Удаляет категорию у пользователя.

        :param user_id: Идентификатор пользователя.
        :param category_id: Идентификатор категории.
        :raises HTTPException: Если пользователь или категория не найдены, или произошла ошибка базы данных.
        """
        try:
            user = await self.user_service.get_user_by_id(user_id)
            category = await self.category_service.get_category_by_id(category_id)

            if category not in user.categories:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This user doesn't have this category",
                )
            user.categories.remove(category)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"An error occurred while removing category from the user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database session error while removing category from the user.",
            )
