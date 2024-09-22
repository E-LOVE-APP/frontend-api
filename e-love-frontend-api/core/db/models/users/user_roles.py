from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..base import BaseModel


class UserRole(BaseModel):
    __tablename__ = "user_role"

    role_name = Column(String(50), nullable=False)

    role = relationship("UserRole", back_populates="user")
