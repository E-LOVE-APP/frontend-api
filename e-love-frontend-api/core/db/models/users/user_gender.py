from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from core.db.models.intermediate_models.user_genders import user_genders_table

from ..base import BaseModel


class UserGender(BaseModel):
    """
    Модель гендера пользователя.

    Атрибуты:
        gender_name (str): Название гендера.
        users (List[User]): Список пользователей, имеющих данный гендер.
    """

    __tablename__ = "user_gender"

    gender_name: Column[str] = Column(String(50), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_genders_table, back_populates="genders"
    )
