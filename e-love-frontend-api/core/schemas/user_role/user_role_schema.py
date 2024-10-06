from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# TODO: Добавить валидаций
"""Basic Users roles model pydantic schema"""


class UserRoleBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the role in UUID format")
    role_name: Optional[str] = Field(
        None, max_length=50, min_length=4, description="Name of the role"
    )

    class Config:
        orm_mode = True


class UserRoleCreate(UserRoleBase):
    role_name: Optional[str] = Field(
        None, max_length=50, min_length=4, description="Name of the role"
    )


class UserRoleUpdate(UserRoleBase):
    role_name: Optional[str] = Field(
        None, max_length=50, min_length=4, description="Name of the role"
    )


class UserRoleOutput(UserRoleBase):
    role_name: Optional[str] = Field(
        None, max_length=50, min_length=4, description="Name of the role"
    )
