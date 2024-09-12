# Module that represents an abstract base model

import uuid
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative, declared_attr
from configuration.database import Base


""" Basic datatable model  """


@as_declarative
class BaseModel(Base):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @declared_attr
    def __tablename__(self, cls):
        return cls.__name__.lower()

    def as_dict(self):
        """
        Returns a map consists of table columns
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
