from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic User Images model pydantic schema"""


class UserImagesBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the user image in UUID format")
    img_url: Optional[UUID] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )

    class Config:
        orm_mode = True


class UserImagesCreate(UserImagesBase):
    img_url: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )
    user_id: UUID = Field(..., description="ID of the user")


class UserImagesUpdate(UserImagesBase):
    img_url: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )


class UserImagesOutput(UserImagesBase):
    img_url: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )
    user_id: str = Field(..., description="ID of the user")


class UserImagesListResponse(BaseModel):
    items: List[UserImagesOutput]
    has_next: bool
    next_token: Optional[str] = None

    class Config:
        orm_mode = True
