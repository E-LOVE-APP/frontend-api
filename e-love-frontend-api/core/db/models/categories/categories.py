from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models.user_categories import user_categories

from ..base import BaseModel


class Categories(BaseModel):
    """
    Модель категорий различных интересов.

    Атрибуты:
        category_name (str): Название категории.
        category_descr (str): Описание категории.
        category_icon (str): Иконка категории.
        posts (List[UserPost]): Список постов в данной категории.
        users (List[User]): Список пользователей, интересующихся данной категорией.
    """

    __tablename__ = "categories"

    category_name: Column[str] = Column(String(50), nullable=False)
    category_descr: Column[str] = Column(String(250), nullable=False)
    category_icon: Column[str] = Column(String(50), nullable=True)

    posts = relationship("UserPost", back_populates="category")

    users = relationship("User", secondary=user_categories, back_populates="categories")
