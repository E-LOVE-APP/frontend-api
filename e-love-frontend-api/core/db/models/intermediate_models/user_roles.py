# models/intermediate_models/user_roles.py
from sqlalchemy import Column, ForeignKey, Table

from ..base import Base

user_roles_table = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("user_role.id"), primary_key=True),
)
