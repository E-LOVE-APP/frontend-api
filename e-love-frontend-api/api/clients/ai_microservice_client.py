from typing import Any, Dict, List, Optional
from uuid import UUID

import aiohttp
from fastapi import File

from exceptions.exception_handler import ExceptionHandler


class AiMicroserviceClient:
    """
    A client to interact with the AI Microservice via REST endpoints.
    """

    def __init__(self, base_url: str, session: Optional[aiohttp.ClientSession] = None):
        self.base_url = base_url.rstrip("/")
        self._session = session

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Internal helper to get or create a session.
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def upload_users_data(self, csv_path: str) -> None:
        """
        Send users data to the ai-sevice

        :param csv_path: path to CSV-file
        :raises Exception: raises exception if something went wrong.
        """
        url = f"{self.base_url}/upload-dataset"
        session = await self._get_session()

        try:
            with open(csv_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("file", f, filename="users.csv", content_type="text/csv")
                # Обрати внимание на контекст @Neeplc (если будешь читать этот коммент) - сейчас мы находимся в контексте, где читаеться файл. Если бы async with session.post был бы за контекстом (один таб влево, например) он бы моментально делал запрос на ai-microservice, что приводило бы к ошибке, так как файл бы просто не успевал бы до конца прочитаться.
                async with session.post(url, data=form) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            ExceptionHandler(e)

    async def get_users_recommendations(
        self, current_user_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get recommended users list from AI-service.

        :param current_user_data: dict with current user data:
                {"user_id": "...", "description": "...", "categories": [...], "viewed_users": [...]}
        :return: list with recommended users ids.
        """
        url = f"{self.base_url}/matching-recommendations"
        session = await self._get_session()

        try:
            async with session.post(url, json=current_user_data) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            ExceptionHandler(e)
            return []
