from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from passlib.hash import bcrypt
from base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    user_descr = Column(String(500), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)

    # Hashing
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    # TODO: добавить сюда доп. атрибуты (role_id, status_id, etc. когда подставные таблицы будут готовы со стороны Вовы)
    # TODO: добавить комментарии классов и методов
    # TODO: добавить категории
