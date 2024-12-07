from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic User Images model pydantic schema"""


class UserImagesBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the user image in UUID format")
    decoded_img: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )

    class Config:
        orm_mode = True


class UserImagesCreate(UserImagesBase):
    decoded_img: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )


class UserImagesUpdate(UserImagesBase):
    decoded_img: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )


class UserImagesOutput(UserImagesBase):
    decoded_img: Optional[str] = Field(
        None, max_length=240, min_length=2, description="Decoded img from user"
    )
