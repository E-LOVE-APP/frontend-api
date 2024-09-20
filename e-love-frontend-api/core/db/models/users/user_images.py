from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from ..base import BaseModel

class UserImages(BaseModel):
     __tablename__ = "user_images"
     
     decoded_img = Column(String(124), nulltable=False)
     
     user_id = Column(ForeignKey("user.id"), nullable=False)
     user = relationship("User", back_populates="image")