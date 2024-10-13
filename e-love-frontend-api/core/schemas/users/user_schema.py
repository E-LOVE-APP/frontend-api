from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# TODO: Добавить валидаций
"""Basic Users-model pydantic schema"""


class UserBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the user in UUID format")
    first_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Last name of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Unique email address of the user")

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    first_name: str = Field(..., max_length=50, min_length=1, description="First name of the user")
    last_name: str = Field(..., max_length=50, min_length=1, description="Last name of the user")
    email: EmailStr = Field(..., description="Unique email address of the user")
    password: str = Field(..., min_length=6, description="Password for the user")


class UserUpdateSchema(UserBase):
    password: Optional[str] = Field(None, min_length=6, description="Password of the user")


class UserOutput(UserBase):
    first_name: str = Field(..., max_length=50, description="First name of the user")
    last_name: str = Field(..., max_length=50, description="Last name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    user_descr: Optional[str] = Field(None, max_length=500, description="Description of the user")


class UsersListResponse(BaseModel):
    users: List[UserOutput]
    has_next: bool
    next_token: Optional[str] = None
