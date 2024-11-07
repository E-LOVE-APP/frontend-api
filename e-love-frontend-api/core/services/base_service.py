import asyncio
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseService:
    """
    Базовый сервисный класс, предоставляющий имплементацию общих CRUD-методов для работы с моделями базы данных.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Инициализация базового сервиса.

        :param db_session: Асинхронная сессия базы данных.
        """
        self.db_session = db_session

    async def get_object_by_id(self, model: Type[ModelType], object_id: UUID) -> ModelType:
        """
        Получает объект модели по его идентификатору.

        :param model: Класс модели базы данных.
        :param object_id: Идентификатор объекта.
        :return: Экземпляр объекта модели.
        :raises HTTPException: Если объект не найден или произошла ошибка базы данных.
        """
        try:
            result = await self.db_session.execute(select(model).where(model.id == str(object_id)))
            obj = result.scalar_one_or_none()
            if not obj:
                raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
            return obj
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while accessing the database."
            )

    async def create_object(
        self,
        model: Type[ModelType],
        data: Dict[str, Any],
        unique_fields: Optional[List[str]] = None,
        preprocess_func: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> ModelType:
        """
        Создает новый объект модели в базе данных.

        :param model: Класс модели базы данных.
        :param data: Данные для создания объекта.
        :param unique_fields: Список полей, которые должны быть уникальными.
        :param preprocess_func: Функция для предобработки данных перед созданием объекта.
        :return: Созданный экземпляр объекта модели.
        :raises HTTPException: Если объект с уникальными полями уже существует или произошла ошибка базы данных.
        """
        try:
            # Проверка на уникальность
            if unique_fields:
                filters = [getattr(model, field) == data[field] for field in unique_fields]
                query = select(model).where(*filters)
                result = await self.db_session.execute(query)
                exists = result.scalar_one_or_none()
                if exists:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{model.__name__} with these unique fields already exists.",
                    )

            # Создание нового объекта
            new_object = model(**data)

            # Предобработка данных
            if preprocess_func:
                if asyncio.iscoroutinefunction(preprocess_func):
                    await preprocess_func(new_object, data)
                else:
                    preprocess_func(new_object, data)

            self.db_session.add(new_object)
            await self.db_session.commit()
            await self.db_session.refresh(new_object)
            return new_object
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while creating the object."
            )

    async def update_object(
        self,
        model: Type[ModelType],
        object_id: UUID,
        data: Union[Dict[str, Any], BaseModel],
        preprocess_func: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> ModelType:
        """
        Обновляет существующий объект модели в базе данных.

        :param model: Класс модели базы данных.
        :param object_id: Идентификатор объекта для обновления.
        :param data: Данные для обновления объекта.
        :param preprocess_func: Функция для предобработки данных перед обновлением объекта.
        :return: Обновленный экземпляр объекта модели.
        :raises HTTPException: Если объект не найден или произошла ошибка базы данных.
        """
        try:
            obj = await self.get_object_by_id(model, object_id)

            if isinstance(data, BaseModel):
                data = data.dict(exclude_unset=True)

            # Предобработка данных
            if preprocess_func:
                if asyncio.iscoroutinefunction(preprocess_func):
                    await preprocess_func(obj, data)
                else:
                    preprocess_func(obj, data)

            # Обновление полей объекта
            for key, value in data.items():
                setattr(obj, key, value)

            self.db_session.add(obj)
            await self.db_session.commit()
            await self.db_session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while updating the object."
            )

    async def delete_object_by_id(self, model: Type[ModelType], object_id: UUID) -> None:
        """
        Удаляет объект модели по его идентификатору.

        :param model: Класс модели базы данных.
        :param object_id: Идентификатор объекта для удаления.
        :raises HTTPException: Если объект не найден или произошла ошибка базы данных.
        """
        try:
            obj_to_delete = await self.get_object_by_id(model, object_id)

            await self.db_session.delete(obj_to_delete)
            await self.db_session.commit()

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail="An error occurred while deleting the object."
            )
