import asyncio
import aiohttp

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from configuration.database import get_db_session
from api.conn_manager.conn_manager import ConnectionManager
from auth.security import authenticator


router = APIRouter()
manager = ConnectionManager()

CHAT_SERVICE_WS_URL = os.getenv("CHAT_SERVICE_WS_URL")
CHAT_SERVICE_AUTH_TOKEN = os.getenv("CHAT_SERVICE_AUTH_TOKEN")

chat_service_ws = None

# TODO: refactor this file


async def connect_to_chat_service():
    global chat_service_ws
    session = aiohttp.ClientSession()
    chat_service_ws = await session.ws_connect(CHAT_SERVICE_WS_URL)
    await chat_service_ws.send_json({"action": "authenticate", "token": CHAT_SERVICE_AUTH_TOKEN})

    async def receive_from_chat_service():
        async for msg in chat_service_ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                action = data.get("action")
                if action == "message_saved":
                    # Обработка подтверждения сохранения сообщения
                    # Можно сохранить ID сообщения или логировать
                    pass
                elif action == "receive_message":
                    sender_id = data["data"].get("sender_id")
                    recipient_id = data["data"].get("recipient_id")
                    content = data["data"].get("content")
                    # Найдите WebSocket клиента для recipient_id и отправьте сообщение
                    recipient_ws = manager.get_connection(recipient_id)
                    if recipient_ws:
                        await recipient_ws.send_text(f"From {sender_id}: {content}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                # add loggining
                break

    asyncio.create_task(receive_from_chat_service())


@router.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket, token: str = Depends(authenticator.authenticate)
):
    """
    WebSocket-эндпоинт для чата, принимающий соединения от Frontend и проксирующий их к Chat-Microservice.
    """
    try:
        payload = token
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Подключение клиента
    await manager.connect(websocket, user_id)

    # Убедитесь, что соединение с Chat-Microservice установлено
    if chat_service_ws is None or chat_service_ws.closed:
        await connect_to_chat_service()

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                recipient_id = message.get("recipient_id")
                content = message.get("content")
                if not recipient_id or not content:
                    await websocket.send_text("Invalid message format.")
                    continue
                # Отправка сообщения в Chat-Microservice через WebSocket
                await chat_service_ws.send_json(
                    {
                        "action": "send_message",
                        "data": {
                            "sender_id": user_id,
                            "recipient_id": recipient_id,
                            "content": content,
                        },
                    }
                )
                # Отправка подтверждения клиенту
                await websocket.send_text("Message sent successfully.")
            except json.JSONDecodeError:
                await websocket.send_text("Invalid JSON format.")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        manager.disconnect(user_id)
