from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseModel


class UserStatus(BaseModel):
    __tablename__ = "user_status"

    status_name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="status")
