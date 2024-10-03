from typing import List
from uuid import UUID

from passlib.hash import bcrypt
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.intermediate_models.user_genders import user_genders_table
from core.db.models.intermediate_models.user_roles import user_roles_table

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

    # INFO: SQLAlchemy при использовании relationship создает специальный объект InstrumentedList,
    # который ведет себя как обычный список Python, но с дополнительной функциональностью
    # для отслеживания изменений и взаимодействия с базой данных.
    status: List["UserStatus"] = relationship("UserStatus", back_populates="users")

    image: List["UserImages"] = relationship("UserImages", back_populates="user")

    posts: List["UserPost"] = relationship("UserPost", back_populates="user")

    logs: List["AuditLogs"] = relationship("AuditLogs", back_populates="user")

    # Many To Many relationships
    genders: List["UserGender"] = relationship(
        "UserGender", secondary=user_genders_table, back_populates="users"
    )
    roles: List["UserRole"] = relationship(
        "UserRole", secondary=user_roles_table, back_populates="users"
    )
    categories: List["Categories"] = relationship(
        "Categories", secondary=user_categories_table, back_populates="users"
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
