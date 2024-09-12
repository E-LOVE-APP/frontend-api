from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from ..base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    user_descr = Column(String(500), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)

    posts = relationship("UserPost", back_populates="user")

    logs = relationship("AuditLogs", back_populates="user")

    categories = relationship("Categories", back_populates="user")

    # Hashing
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    # TODO: добавить сюда доп. атрибуты (role_id, status_id, etc. когда подставные таблицы будут готовы со стороны Вовы)
    # TODO: добавить комментарии классов и методов
