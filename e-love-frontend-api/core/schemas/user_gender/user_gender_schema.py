from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic User gender model pydantic schema"""


class UserGenderBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the gender in UUID format")
    gender_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the gender"
    )

    class Config:
        orm_mode = True


class UserGenderCreate(UserGenderBase):
    gender_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the gender"
    )


class UserGenderUpdate(UserGenderBase):
    gender_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the gender"
    )


class UserGenderOutput(UserGenderBase):
    gender_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the gender"
    )
