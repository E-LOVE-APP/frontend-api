from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import validates
from base import BaseModel


class Categories(BaseModel):
    __tablename__ = "categories"

    category_name = Column(String(50), nullable=False)
    category_descr = Column(String(250), nullable=False)
    # Это атрибут для фронтенда, возможно нужен будет в будущем, но это 50 на 50 (если надо - объясню; если что мы всегда сможем этот атрибут удалить)
    category_icon = Column(String(50), nullable=True)
