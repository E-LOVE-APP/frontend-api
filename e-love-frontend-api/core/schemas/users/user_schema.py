from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserOutput(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
