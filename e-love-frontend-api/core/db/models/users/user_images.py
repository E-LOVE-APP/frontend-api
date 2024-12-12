from typing import List
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from ..base import BaseModel


class UserImages(BaseModel):
    """
    SQLAlchemy model for storing user images.

    Attributes:
        img_url: URL of the user's image.
        user_id: ID of the user to whom the image belongs.
        user: Relationship to the User model.
    """

    __tablename__ = "user_images"

    img_url: Column[str] = Column(String(240), nullable=False)
    user_id: Column[UUID] = Column(ForeignKey("user.id"), nullable=False)
    user: Mapped[List["User"]] = relationship("User", back_populates="image", uselist=True)
