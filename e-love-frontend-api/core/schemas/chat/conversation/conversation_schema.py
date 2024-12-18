from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional


class ConversationBase(BaseModel):
    other_user_id: UUID
