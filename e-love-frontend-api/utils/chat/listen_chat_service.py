import json

import aiohttp
from fastapi import WebSocket


async def listen_chat_service(
    chat_service_ws: aiohttp.ClientWebSocketResponse, client_ws: WebSocket
):
    """
    Reads messages (as JSON) from Chat-Microservice WebSocket
    and forwards them to the client (Frontend) as JSON.
    """
    async for msg in chat_service_ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            raw_text = msg.data  # это str
            try:
                json_data = json.loads(raw_text)
                await client_ws.send_json(json_data)
            except json.JSONDecodeError:
                await client_ws.send_text(raw_text)
        elif msg.type == aiohttp.WSMsgType.BINARY:
            await client_ws.send_bytes(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

    await client_ws.close()
