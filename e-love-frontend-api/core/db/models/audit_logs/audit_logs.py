from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import validates
from base import BaseModel


class AuditLogs(BaseModel):
    __tablename__ = "audit_logs"

    # TODO: add user_id
    # TODO: check timezones
    last_login = Column(DateTime(timezone=True), nullable=False)
    endpoint = Column(String(150), nullable=False)
    method = Column(String(50), nullable=False)
    result = Column(String(50), nullable=False)
