# models/intermediate_models/user_genders.py
from sqlalchemy import Column, ForeignKey, Table

from ..base import Base

user_genders_table = Table(
    "user_genders",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("gender_id", ForeignKey("user_gender.id"), primary_key=True),
)
