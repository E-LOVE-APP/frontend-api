# type: ignore
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from core.db.models.intermediate_models.posts_categories import posts_categories_table

from ..base import BaseModel


# TODO: add docstring & types
class UserPost(BaseModel):
    __tablename__ = "user_post"

    post_title = Column(String(250), nullable=False)
    post_descr = Column(String(1000), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts", lazy="selectin")
    created_at = Column(DateTime, default=func.now())

    category = relationship(
        "Categories", secondary=posts_categories_table, back_populates="posts", lazy="selectin"
    )
