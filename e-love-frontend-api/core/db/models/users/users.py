from typing import List
from uuid import UUID

from passlib.hash import bcrypt
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from core.db.models.audit_logs.audit_logs import AuditLogs
from core.db.models.categories.categories import Categories
from core.db.models.intermediate_models.posts_categories import posts_categories_table
from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.intermediate_models.user_genders import user_genders_table
from core.db.models.intermediate_models.user_roles import user_roles_table
from core.db.models.posts.user_post import UserPost
from core.db.models.users.user_gender import UserGender
from core.db.models.users.user_images import UserImages
from core.db.models.users.user_interaction import UserInteraction
from core.db.models.users.user_role import UserRole
from core.db.models.users.user_status import UserStatus

from ..base import BaseModel


class User(BaseModel):
    """
    Модель пользователя, представляющая информацию о пользователе в системе.

    Атрибуты:
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        user_descr (str): Описание пользователя.
        email (str): Электронная почта пользователя.
        password_hash (str): Хеш пароля пользователя.
        genders (List[UserGender]): Список гендеров пользователя.
        roles (List[UserRole]): Список ролей пользователя.
        categories (List[Category]): Список интересов пользователя.
        image (UserImages): Связь с изображениями пользователя.
        posts (List[UserPost]): Список постов пользователя.
        logs (List[AuditLogs]): Журналы действий пользователя.
    """

    __tablename__ = "user"

    first_name: Column[str] = Column(String(50), nullable=False)
    last_name: Column[str] = Column(String(50), nullable=False)
    user_descr: Column[str] = Column(String(500), nullable=True)
    email: Column[str] = Column(String(255), unique=True, nullable=False)
    password_hash: Column[str] = Column(String(128), nullable=True)

    status_id: Column[UUID] = Column(ForeignKey("user_status.id"), nullable=False)

    status: Mapped["UserStatus"] = relationship("UserStatus", back_populates="users")

    # TODO: change the name to 'images'; Probably should also do it like M to M relationship
    image: Mapped[List["UserImages"]] = relationship("UserImages", back_populates="user")

    posts: Mapped[List["UserPost"]] = relationship(
        "UserPost", back_populates="user", lazy="selectin"
    )

    # TODO: delete AuditLogs table (UC-35)
    logs: Mapped["AuditLogs"] = relationship("AuditLogs", back_populates="user")

    # Many To Many relationships
    genders: Mapped[List["UserGender"]] = relationship(
        "UserGender", secondary=user_genders_table, back_populates="users", lazy="selectin"
    )

    roles: Mapped[List["UserRole"]] = relationship(
        "UserRole", secondary=user_roles_table, back_populates="users", lazy="selectin"
    )

    categories: Mapped[List["Categories"]] = relationship(
        "Categories", secondary=user_categories_table, back_populates="users", lazy="selectin"
    )

    interactions_sent: Mapped[List["UserInteraction"]] = relationship(
        "UserInteraction", foreign_keys="[UserInteraction.user_id]", back_populates="user"
    )

    interactions_received: Mapped[List["UserInteraction"]] = relationship(
        "UserInteraction",
        foreign_keys="[UserInteraction.target_user_id]",
        back_populates="target_user",
    )

    def set_password(self, password: str) -> None:
        """
        Устанавливает хеш пароля для пользователя.

        Args:
            password (str): Пароль в открытом виде.
        """

        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """
        Проверяет соответствие введенного пароля и сохраненного хеша.

        Args:
            password (str): Введенный пароль.

        Returns:
            bool: True, если пароли совпадают, иначе False.
        """
        return bcrypt.verify(password, self.password_hash)
