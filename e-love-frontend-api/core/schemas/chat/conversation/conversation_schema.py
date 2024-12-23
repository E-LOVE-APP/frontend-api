from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
    other_user_id: UUID
