# type: ignore
from passlib.hash import bcrypt
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models import (
    user_categories_table,
    user_genders_table,
    user_roles_table,
)

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

    status_id = Column(ForeignKey("user_status.id"), nullable=False)
    status = relationship("UserStatus", back_populates="users")

    image = relationship("UserImages", back_populates="user")

    posts = relationship("UserPost", back_populates="user")

    logs = relationship("AuditLogs", back_populates="user")

    # Many To Many relationships
    genders = relationship("UserGender", secondary=user_genders_table, back_populates="users")
    roles = relationship("UserRole", secondary=user_roles_table, back_populates="users")
    categories = relationship("Categories", secondary=user_categories_table, back_populates="users")

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
