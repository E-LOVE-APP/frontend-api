from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

"""Pydantic schemas for User Interactions."""


# TODO: переместить в UTILS;
class InteractionType(str, Enum):
    """Enumeration of possible interaction types."""

    MATCH = "MATCH"
    REJECT = "REJECT"


class UserInteractionBase(BaseModel):
    """Base model for user interactions with common fields."""

    interaction_type: InteractionType = Field(
        ..., description="Type of interaction (match or reject)"
    )
    user_id: UUID = Field(..., description="ID of the current user that triggered the interaction")
    target_user_id: UUID = Field(
        ..., description="ID of the target user the interaction is aimed at"
    )

    class Config:
        orm_mode = True
        extra = "forbid"


class UserInteractionCreate(UserInteractionBase):
    """Schema for creating a new user interaction."""

    pass  # All fields are inherited and required.


class UserInteractionUpdate(BaseModel):
    """Schema for updating an existing user interaction."""

    interaction_type: Optional[InteractionType] = Field(
        None, description="Updated type of interaction (match or reject)"
    )

    class Config:
        extra = "forbid"


class UserInteractionOutput(UserInteractionBase):
    """Schema for displaying user interaction data."""

    id: UUID = Field(..., description="ID of the user-interaction entity in UUID format")

    class Config:
        orm_mode = True
        extra = "forbid"


class UserInteractionsListResponse(BaseModel):
    """Schema for a list of user interactions with pagination information."""

    user_interaction: List[UserInteractionOutput]
    has_next: bool
    next_token: Optional[str] = None

    class Config:
        extra = "forbid"
