import os
from uuid import UUID

import aiohttp


async def connect_to_chat_service(conversation_id: UUID):
    """"""

    base_url = os.getenv("CHAT_SERVICE_CONNECT_URL_LOCAL")
    ws_url = f"{base_url}/{conversation_id}"
    session = aiohttp.ClientSession()
    chat_service_ws = await session.ws_connect(ws_url)
    return chat_service_ws
