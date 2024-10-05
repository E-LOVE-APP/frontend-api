# core/services/base_service.py
# types: ignore
# type: ignore

import uuid
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


# TODO: add docstrings
class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_object_by_id(self, model, object_id: UUID):

        object_id_str = str(object_id)  # Преобразуем UUID в строку с дефисами

        result = await self.db_session.execute(select(model).where(model.id == object_id_str))

        obj = result.scalar_one_or_none()

        if not obj:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

        return obj

    async def delete_object_by_id(self, model, object_id: UUID):

        object_id_str = str(object_id)
        obj_to_delete = await self.get_object_by_id(model, object_id_str)

        if not obj_to_delete:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

        await self.db_session.delete(obj_to_delete)
        await self.db_session.commit()
