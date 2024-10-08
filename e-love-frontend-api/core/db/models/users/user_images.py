from typing import List
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from ..base import BaseModel


class UserImages(BaseModel):
    __tablename__ = "user_images"

    decoded_img: Column[str] = Column(String(124), nullable=False)

    user_id: Column[UUID] = Column(ForeignKey("user.id"), nullable=False)
    user: Mapped[List["User"]] = relationship("User", back_populates="image", uselist=True)
