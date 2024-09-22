from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseModel


class Categories(BaseModel):
    __tablename__ = "categories"

    category_name = Column(String(50), nullable=False)
    category_descr = Column(String(250), nullable=False)
    category_icon = Column(String(50), nullable=True)

    posts = relationship("UserPost", back_populates="category")
