from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..base import BaseModel


class UserGender(BaseModel):
    __tablename__ = "user_gender"

    gender_name = Column(String(50), nullable=False)

    gender = relationship("User", back_populates="gender")
