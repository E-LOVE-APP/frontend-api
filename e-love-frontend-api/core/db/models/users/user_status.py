from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from ..base import BaseModel


class UserStatus(BaseModel):
    __tablename__ = "user_status"

    status_name: Column[str] = Column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship("User", back_populates="status")
