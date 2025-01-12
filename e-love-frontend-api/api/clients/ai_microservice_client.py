from uuid import UUID
from fastapi import File
from typing import Optional, Dict, Any, List

import aiohttp
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
            form = aiohttp.FormData()
            with open(csv_path, "rb") as f:
                form.add_field(name="file", value=f, filename="users.csv", content_type="text/csv")

            async with session.post(url, data=form) as response:
                response.raise_for_status()
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
