from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


class UserImagesBase(BaseModel):
    """
    Base Pydantic schema for user images, including shared fields.

    Attributes:
        id: Unique identifier of the user image in UUID format.
        img_url: URL of the user's image.
    """

    id: Optional[UUID] = Field(None, description="An ID of the user image in UUID format")
    img_url: Optional[HttpUrl] = Field(None, description="URL of the user's image")

    class Config:
        from_attributes = True


class UserImagesCreate(UserImagesBase):
    """
    Pydantic schema for creating a new user image.

    Attributes:
        img_url: URL of the new user's image.
        user_id: ID of the user to whom the image belongs.
    """

    img_url: HttpUrl = Field(..., description="URL of the user's image")
    user_id: UUID = Field(..., description="ID of the user")


class UserImagesUpdate(UserImagesBase):
    """
    Pydantic schema for updating an existing user image.

    Attributes:
        img_url: URL of the user's image (optional for updates).
    """

    img_url: Optional[HttpUrl] = Field(None, description="URL of the user's image")


class UserImagesOutput(UserImagesBase):
    """
    Pydantic schema for outputting user image data.

    Attributes:
        img_url: URL of the user's image.
        user_id: ID of the user to whom the image belongs.
    """

    img_url: Optional[HttpUrl] = Field(None, description="URL of the user's image")
    user_id: str = Field(..., description="ID of the user")


class UserImagesListResponse(BaseModel):
    """
    Pydantic schema for paginated responses of user images.

    Attributes:
        items: List of user images.
        has_next: Boolean indicating if there are more images to fetch.
        next_token: Token for fetching the next page of images.
    """

    items: List[UserImagesOutput]
    has_next: bool
    next_token: Optional[str] = None

    class Config:
        from_attributes = True
