from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from core.schemas.users_categories.users_categories_schema import CategoryOutput
from core.schemas.posts.user_post_schema import PostOutput
from core.db.models.posts.user_post import UserPost

"""Pydantic schemas for Users."""


class UserBase(BaseModel):
    """Base user model with common fields."""

    first_name: str = Field(..., max_length=50, min_length=1, description="First name of the user")
    last_name: str = Field(..., max_length=50, min_length=1, description="Last name of the user")
    email: EmailStr = Field(..., description="Unique email address of the user")

    class Config:
        orm_mode = True
        from_attributes = True
        extra = "forbid"


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=6, description="Password for the user")

    class Config:
        extra = "forbid"


class UserUpdate(UserBase):
    """Schema for updating an existing user."""

    first_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, max_length=50, min_length=1, description="Last name of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Unique email address of the user")
    password: Optional[str] = Field(None, min_length=6, description="Password for the user")

    class Config:
        extra = "forbid"


class UserOutput(UserBase):
    """Schema for displaying user data."""

    id: UUID = Field(..., description="ID of the user in UUID format")
    user_descr: Optional[str] = Field(None, max_length=500, description="Description of the user")
    categories: Optional[List[CategoryOutput]] = None
    posts: Optional[List[PostOutput]] = None

    class Config:
        orm_mode = True
        extra = "forbid"
        from_attributes = True

    @validator("posts", pre=True, each_item=True)
    def convert_posts(cls, v):
        if isinstance(v, UserPost):
            return PostOutput.from_orm(v)
        return v


class UsersListResponse(BaseModel):
    """Schema for a list of users with pagination information."""

    users: List[UserOutput]
    has_next: bool
    next_token: Optional[str] = None

    class Config:
        extra = "forbid"


class UsersMatchingListResponse(BaseModel):
    matching_users: List[UserOutput]
    total: int
    next_token: Optional[str] = None

    class Config:
        extra = "forbid"
