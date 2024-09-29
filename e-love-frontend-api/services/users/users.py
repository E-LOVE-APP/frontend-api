# Service class for the 'User' model
import logging
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from configuration.database import get_db_session
from core.db.models.users.users import User
from core.schemas.users.user_schema import UserCreate, UserUpdate, UserOutput

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session  # Объявление параметра (или атрибута другими словами) класса

    # Любой метод сервиса оборачиваем для начала в try-catch блоки. Это делает код более устойчивым к сбоям и более чистым.
    # Пока что, у нас нету кастомного класса отлова ошибок, по-этому пока будем 'ловить' только Exception. После того, как
    # я настрою Auth0, я создам класс с кастом-ошибками, которые будут детальнее показывать, что за ошибка и произошла (пока что будет просто везде 500, некий универсальный статус)

    # Пока что тут так же не хватает асинхронности, но я ее настрою. Пока старайся вникнуть в код и понимать, что тут проихсодит. Держи так же в голове, что код позже может поменяться.

    def create_user(self, user_data: UserCreate) -> UserOutput:
        try:
            # Проверка, существует ли пользователь с таким email
            user_exists = self.db_session.query(User).filter(User.email == user_data.email).first()
            if user_exists:
                logger.warning(
                    f"Someone trying to create a user with existing email: {user_data.email}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already taken by someone",
                )

            new_user = User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
            )

            new_user.set_password(user_data.password)

            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)

            return new_user

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )

    # TODO: Сюда в параметр нужно добавить проверку не просто по int, а по UUID
    def get_user_by_id(self, user_id: int) -> UserOutput:
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserOutput.from_orm(user)

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )

    # TODO: Тут нету кастомной пагинации, я ее тоже позже добавлю на проект
    def get_users_list(
        self, page: int = 1, size: int = 0, limit: int = 10, email: Optional[str] = None
    ) -> List[User]:
        try:
            query = self.db_session.query(user)
            if email:
                query = query.filter(User.email == email)
            users = (
                query.options(selectinload(User.roles))
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )
            return users
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )

    def update_user(self, user_id: int, update_data: UserUpdate) -> UserOutput:
        try:
            user = self.get_user_by_id(user_id)
            if "password" in update_data:
                user.set_password(update_data.pop("password"))
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db_session.commit()
            self.db_session.refresh(user)
            return user
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )

    def delete_user(self, user_id: int) -> None:
        try:
            user = self.get_user_by_id(user_id)
            self.db_session.delete(user)
            self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )
