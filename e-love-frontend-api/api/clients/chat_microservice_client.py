from typing import Any, Dict, List, Optional
from uuid import UUID

import aiohttp


class ChatMicroserviceClient:
    """
    A client to interact with the Chat Microservice via REST endpoints.
    Follows the Single Responsibility principle: one class for all chat-related requests.
    """

    def __init__(self, base_url: str, session: Optional[aiohttp.ClientSession] = None):
        """
        Initialize ChatMicroserviceClient with a base URL.

        :param base_url: The root URL of ChatMicroservice (e.g. "http://chat-service-api:8081/v1")
        :param session: Optionally pass an existing aiohttp.ClientSession.
        """
        self.base_url = base_url.rstrip("/")
        self._session = session

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Internal helper to get or create a session.
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def create_conversation(self, user_first_id: str, user_second_id: str) -> Dict[str, Any]:
        """
        Create a conversation between two users (UUID strings).
        Returns the conversation data.
        """
        url = f"{self.base_url}/conversations"
        payload = {
            "user_first_id": user_first_id,
            "user_second_id": user_second_id,
        }
        session = await self._get_session()
        async with session.post(url, json=payload) as resp:
            if resp.status not in (200, 201):
                text = await resp.text()
                raise Exception(f"Failed to create conversation: {resp.status} {text}")
            return await resp.json()

    async def get_conversation(self, conversation_id: UUID) -> Dict[str, Any]:
        """
        Fetch a conversation by its ID.
        """
        url = f"{self.base_url}/conversations/{conversation_id}"
        session = await self._get_session()
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Failed to get conversation: {resp.status} {text}")
            return await resp.json()

    async def delete_conversation(self, conversation_id: UUID) -> Dict[str, Any]:
        """
        Soft-delete a conversation by ID.
        """
        url = f"{self.base_url}/conversations/{conversation_id}"
        session = await self._get_session()
        async with session.delete(url) as resp:
            if resp.status not in [200, 204]:
                text = await resp.text()
                raise Exception(f"Failed to delete conversation: {resp.status} {text}")
            if resp.status == 200:
                return await resp.json()
            return {}

    async def create_message(
        self, conversation_id: str, sender_id: str, recipient_id: str, content: str
    ) -> Dict[str, Any]:
        """
        Create a new message in a conversation.
        """
        url = f"{self.base_url}/messages"
        payload = {
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "content": content,
        }
        session = await self._get_session()
        async with session.post(url, json=payload) as resp:
            if resp.status not in (200, 201):
                text = await resp.text()
                raise Exception(f"Failed to create message: {resp.status} {text}")
            return await resp.json()

    async def update_message(self, message_id: UUID, status: str) -> Dict[str, Any]:
        """
        Update a message status.
        """
        url = f"{self.base_url}/messages/{message_id}"
        session = await self._get_session()
        payload = {"status": status}
        async with session.put(url, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Failed to update message: {resp.status} {text}")
            return await resp.json()

    async def delete_message(self, message_id: UUID) -> None:
        """
        Delete a message by ID.
        """
        url = f"{self.base_url}/messages/{message_id}"
        session = await self._get_session()
        async with session.delete(url) as resp:
            if resp.status not in (200, 204):
                text = await resp.text()
                raise Exception(f"Failed to delete message: {resp.status} {text}")

    async def get_conversation_messages(self, conversation_id: UUID) -> List[Dict[str, Any]]:
        """
        Retrieve the list of messages for the specified conversation.
        Returns a list of message objects as dictionaries.
        """
        url = f"{self.base_url}/messages/{conversation_id}"
        session = await self._get_session()
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Failed to get messages: {resp.status} {text}")
            return await resp.json()
