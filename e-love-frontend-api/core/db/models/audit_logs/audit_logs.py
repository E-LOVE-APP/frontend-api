# type: ignore
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from ..base import BaseModel


class AuditLogs(BaseModel):
    __tablename__ = "audit_logs"

    # TODO: check timezones
    last_login = Column(DateTime(timezone=True), nullable=False)
    endpoint = Column(String(150), nullable=False)
    method = Column(String(50), nullable=False)
    result = Column(String(50), nullable=False)

    user_id: str = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="logs")
