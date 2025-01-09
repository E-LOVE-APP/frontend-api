import base64
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

T = TypeVar("T")


class Paginator(Generic[T]):
    """
    Обобщенный класс пагинатора, который реализует пагинацию на основе курсора для моделей SQLAlchemy ORM.

    Этот пагинатор предназначен для работы с асинхронными сессиями SQLAlchemy и моделями,
    которые имеют поля 'created_at' и 'id'. Он использует эти поля для генерации и декодирования курсоров пагинации.

    Атрибуты:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy.
        model (Type[T]): Класс модели SQLAlchemy ORM.
        limit (int): Максимальное количество элементов для возврата на странице.
    """

    def __init__(self, db_session: AsyncSession, model: Type[T], limit: int = 10):
        """
        Инициализирует экземпляр Paginator.

        Аргументы:
            db_session (AsyncSession): Асинхронная сессия SQLAlchemy для использования в запросах.
            model (Type[T]): Класс модели SQLAlchemy ORM для пагинации.
            limit (int, optional): Максимальное количество элементов для возврата на странице. По умолчанию 10.
        """
        self.db_session = db_session
        self.model = model
        self.limit = limit

    def encode_token(self, last_created_at: str, last_id: str) -> str:
        """
        Кодирует курсор пагинации в строку base64.

        Аргументы:
            last_created_at (str): Строка даты и времени в формате ISO поля 'created_at' последнего элемента.
            last_id (str): Строковое представление поля 'id' последнего элемента.

        Возвращает:
            str: Строка, закодированная в base64, представляющая курсор пагинации.
        """
        token_dict = {"created_at": last_created_at, "id": last_id}
        token_str = json.dumps(token_dict)
        token_bytes = token_str.encode("utf-8")
        encoded_token = base64.urlsafe_b64encode(token_bytes).decode("utf-8")
        return encoded_token

    def decode_token(self, token: str) -> Dict[str, str]:
        """
        Декодирует курсор пагинации из строки base64.

        Аргументы:
            token (str): Строка, закодированная в base64, представляющая курсор пагинации.

        Возвращает:
            Dict[str, str]: Словарь, содержащий ключи 'created_at' и 'id' с их значениями.

        Вызывает:
            ValueError: Если токен недействителен или не может быть декодирован.
        """
        try:
            token_bytes = base64.urlsafe_b64decode(token.encode("utf-8"))
            token_str = token_bytes.decode("utf-8")
            token_dict = json.loads(token_str)
            return token_dict
        except Exception:
            raise ValueError("Invalid token")

    # TODO: зарефакторить, слишком много информации для чтения глазами. Разбить на отдельные функции по SOLID-принципам.
    async def paginate_query(
        self,
        base_query: Select,
        next_token: Optional[str] = None,
        filters: Optional[Any] = None,
        order_by: Optional[List[Any]] = None,
        model_name: str = "items",
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Выполняет пагинацию указанного запроса SQLAlchemy с использованием пагинации на основе курсора.

        Аргументы:
            base_query (Select): Базовый запрос SQLAlchemy для пагинации.
            next_token (Optional[str], optional): Курсор пагинации с предыдущей страницы. По умолчанию None.
            filters (Optional[Any], optional): Дополнительные фильтры для применения к запросу. По умолчанию None.
            order_by (Optional[List[Any]], optional): Пользовательская сортировка для запроса. По умолчанию None.
            model_name (str, optional): Имя ключа для списка элементов в ответе. По умолчанию "items".
            limit (Optional[int], optional): Максимальное количество элементов для возврата на странице. Если указано, переопределяет limit экземпляра. По умолчанию None.

        Возвращает:
            Dict[str, Any]: Словарь, содержащий:
                - model_name (List[T]): Список элементов для текущей страницы.
                - "has_next" (bool): Флаг, указывающий, есть ли следующая страница.
                - "next_token" (Optional[str]): Курсор пагинации для следующей страницы или None, если страниц больше нет.

        Вызывает:
            ValueError: Если предоставленный next_token недействителен.
        """
        if limit is not None:
            self.limit = limit

        query = base_query

        # Применяем дополнительные фильтры, если они есть
        if filters is not None:
            query = query.where(filters)

        # Применяем пагинацию на основе курсора, если предоставлен next_token
        if next_token:
            token_data = self.decode_token(next_token)
            last_created_at = datetime.fromisoformat(token_data["created_at"])
            last_id = uuid.UUID(token_data["id"])

            # Фильтруем запрос для получения элементов после позиции курсора
            query = query.where(
                (self.model.created_at > last_created_at)
                | ((self.model.created_at == last_created_at) & (self.model.id > last_id))
            )

        # Применяем сортировку к запросу
        if order_by is not None:
            query = query.order_by(*order_by)
        else:
            # Сортировка по умолчанию: по возрастанию 'created_at' и 'id'
            query = query.order_by(asc(self.model.created_at), asc(self.model.id))

        # Запрашиваем на один элемент больше, чтобы определить, есть ли следующая страница
        query = query.limit(self.limit + 1)

        result = await self.db_session.execute(query)
        items = result.scalars().all()

        # Определяем, есть ли следующая страница
        has_next = len(items) > self.limit
        if has_next:
            # Убираем лишний элемент, используемый для проверки наличия следующей страницы
            items = items[: self.limit]

        # Генерируем next_token, если есть следующая страница
        next_token_value = None
        if has_next:
            last_item = items[-1]
            last_created_at_str = last_item.created_at.isoformat()
            last_item_id = str(last_item.id)
            next_token_value = self.encode_token(last_created_at_str, last_item_id)

        response = {
            model_name: items,
            "has_next": has_next,
            "next_token": next_token_value,
        }

        return response

    # TODO: refactor - chatGPT generated code!
    # def in_memory_paginate(items: list[dict], next_token: Optional[str], limit: int) -> dict:
    #     """
    #     items: уже отсортированный массив (score DESC, user_id ASC)
    #         ИЛИ наоборот, главное, чтобы был единый порядок
    #     next_token: курсор base64, может быть None
    #     limit: сколько хотим вернуть
    #     return: {
    #     "items": [...],
    #     "has_next": bool,
    #     "next_token": str or None
    #     }
    #     """
    #     # 1) Раскодируем курсор
    #     start_index = 0
    #     last_score = None
    #     last_user_id = None
    #     if next_token:
    #         token_data = decode_token(next_token)
    #         last_score = float(token_data["score"])
    #         last_user_id = token_data["user_id"]
    #         # 2) находим, где в массиве items находится этот курсор
    #         #    допустим items отсортированы по score DESC, user_id ASC
    #         for idx, it in enumerate(items):
    #             score = it["final_score"]
    #             uid = it["user_id"]
    #             # сравниваем, пока не найдём позицию > / == ...
    #             # Нужно аккуратно определить условие
    #             # if (score == last_score and uid == last_user_id):
    #             #    start_index = idx + 1
    #             #    break
    #             # но если вы в cursor-based подходе делаете
    #             # (score < last_score) or (score==last_score & uid>last_user_id)
    #             # тогда нужно найти индекс первого элемента, который *идёт после* этого курсора
    #             # ...
    #         # start_index — позиция, с которой начинаем страницу

    #     # 3) Берём slice
    #     end_index = start_index + limit
    #     page_items = items[start_index:end_index]

    #     has_next = end_index < len(items)
    #     new_next_token = None
    #     if has_next:
    #         # последний элемент на странице
    #         last_elem = page_items[-1]
    #         new_next_token = encode_token(
    #             {"score": str(last_elem["final_score"]), "user_id": last_elem["user_id"]}
    #         )

    #     return {"items": page_items, "has_next": has_next, "next_token": new_next_token}
