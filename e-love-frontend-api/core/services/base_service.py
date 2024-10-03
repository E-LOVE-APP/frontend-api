# core/services/base_service.py
# types: ignore
# type: ignore

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # TODO: add typization
    async def get_object_by_id(self, model, object_id: UUID):
        result = await self.db_session.execute(select(model).where(model.id == object_id))
        obj = result.scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return obj
