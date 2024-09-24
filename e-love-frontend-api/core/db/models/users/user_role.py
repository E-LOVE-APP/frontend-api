from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models.user_roles import user_roles

from ..base import BaseModel


class UserRole(BaseModel):
    """
    Модель роли пользователя.

    Атрибуты:
        role_name (str): Название роли.
        users (List[User]): Список пользователей, имеющих данную роль.
    """

    __tablename__ = "user_role"

    role_name: Column[str] = Column(String(50), nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")
