from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel


class UserImages(BaseModel):
    __tablename__ = "user_images"

    decoded_img = Column(String(124), nullable=False)

    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="image")
