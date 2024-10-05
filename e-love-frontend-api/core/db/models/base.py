# Module that represents an abstract base model

import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import declared_attr

from configuration.database import Base


class BaseModel(Base):
    __abstract__ = True

    # TODO: рассмотреть вопрос по касту этого Column до binary-id в целях экономии места в БД ?
    id = Column(
        String(36),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        """
        Returns a map consists of table columns
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
