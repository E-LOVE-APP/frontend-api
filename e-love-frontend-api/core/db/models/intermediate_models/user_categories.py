# models/intermediate_models/user_categories.py
from sqlalchemy import Column, ForeignKey, Table

from ..base import Base

user_categories_table = Table(
    "user_categories",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)
