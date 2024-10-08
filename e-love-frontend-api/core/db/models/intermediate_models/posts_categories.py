# models/intermediate_models/posts_categories.py
from sqlalchemy import Column, ForeignKey, Table

from ..base import Base

posts_categories_table = Table(
    "posts_categories",
    Base.metadata,
    Column("post_id", ForeignKey("user_post.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)
