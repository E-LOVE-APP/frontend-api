from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from ..base import BaseModel

class UserGender(BaseModel):
     __tablename__ = "user_gender"
     
     gender_name = Column(String(50), nullable=False)

     user_id = Column(ForeignKey("user.id"), nullable=False)
     user = relationship("User", back_populates="gender")
