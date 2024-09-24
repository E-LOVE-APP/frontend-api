# type: ignore
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models.user_genders import user_genders

from ..base import BaseModel


class UserGender(BaseModel):
    """
    Модель гендера пользователя.

    Атрибуты:
        gender_name (str): Название гендера.
        users (List[User]): Список пользователей, имеющих данный гендер.
    """

    __tablename__ = "user_gender"

    gender_name: Column[str] = Column(String(50), nullable=False)

    users = relationship("User", secondary=user_genders, back_populates="genders")
