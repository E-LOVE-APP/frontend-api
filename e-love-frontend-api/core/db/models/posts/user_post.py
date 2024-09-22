from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..base import BaseModel


class UserPost(BaseModel):
    __tablename__ = "user_post"

    post_title = Column(String(250), nullable=False)
    post_descr = Column(String(1000), nullable=False)

    category_id = Column(ForeignKey("categories.id"), nullable=False)
    category = relationship("Categories", back_populates="posts")

    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts")
