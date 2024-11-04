from typing import List
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from ..base import BaseModel


class UserInteraction(BaseModel):
    """
    Модель пользовательского взаимодействия с другим пользователем,
    которое сохраняет эту информацию в системе.

    Атрибуты:
       user_id (UUID): id текущего пользователя.
       target_user_id (UUID): id пользователя, с которым произошло взаимодействие ОТ текущего пользователя.
       interaction_type (INTERACTION_TYPE): Тип взаимодействия пользователя (match/skip)
    """

    __tablename__ = "user_interaction"

    user_id: Column[UUID] = Column(ForeignKey("user.id"), nullable=False)

    target_user_id: Column[UUID] = Column(ForeignKey("user.id"), nullable=False)

    interaction_type: Column[str] = Column(String(10), nullable=False)

    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="interactions_sent"
    )

    target_user: Mapped["User"] = relationship(
        "User", foreign_keys=[target_user_id], back_populates="interactions_received"
    )
