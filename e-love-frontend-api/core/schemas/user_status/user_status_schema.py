from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# TODO: Добавить валидаций
"""Basic User status model pydantic schema"""

class UserStatusBase(BaseModel):
    id: Optional[UUID] = Field(None, description="An id of the user status in UUID format")
    status_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the user status"
    )

    class Config:
        orm_mode = True


class UserStatusCreate(UserStatusBase):
    status_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the user status"
    )


class UserStatusUpdate(UserStatusBase):
    status_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the user status"
    )


class UserStatusOutput(UserStatusBase):
    status_name: Optional[str] = Field(
        None, max_length=50, min_length=2, description="Name of the user status"
    )
