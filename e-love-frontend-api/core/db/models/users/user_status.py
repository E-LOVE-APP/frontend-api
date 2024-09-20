from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from ..base import BaseModel

class UserStatus(BaseModel):
     __tablename__ = "user_status"
     
     status_name = Column(String(50), nulltable=False)
     
     user_id = Column(ForeignKey("user.id"), nullable=False)
     user = relationship("User", back_populates="status")