import asyncio
import json
import os
from uuid import UUID

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from api.conn_manager.conn_manager import ConnectionManager
from auth.security import authenticator
from configuration.database import get_db_session
from core.schemas.chat.conversation.conversation_schema import ConversationBase

router = APIRouter()
manager = ConnectionManager()

# TODO: make a condition here where we want to pick a variable depends on prod/local env (in the future)
CHAT_SERVICE_CREATE_CONVERSATION_URL_LOCAL = os.getenv("CHAT_SERVICE_CREATE_CONVERSATION_URL_LOCAL")
CHAT_SERVICE_CONNECT_URL_LOCAL = os.getenv("CHAT_SERVICE_CONNECT_URL_LOCAL")
CHAT_SERVICE_AUTH_TOKEN = os.getenv("CHAT_SERVICE_AUTH_TOKEN")

chat_service_ws = None

# TODO: refactor this file


# TODO: add local/prod conditional connection
# TODO: add try/catch block
async def connect_to_chat_service(conversation_id: UUID):
    global chat_service_ws
    ws_url = CHAT_SERVICE_CONNECT_URL_LOCAL
    session = aiohttp.ClientSession()
    chat_service_ws = await session.ws_connect(ws_url)
    await chat_service_ws.send_json({"action": "authenticate", "token": CHAT_SERVICE_AUTH_TOKEN})

    async def receive_from_chat_service():
        async for msg in chat_service_ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                action = data.get("action")
                if action == "message_saved":
                    sender_id = data["data"]["sender_id"]
                    recipient_id = data["data"]["recipient_id"]
                    content = data["data"]["content"]

                    recipient_ws = manager.get_connection(recipient_id)
                    if recipient_ws:
                        await recipient_ws.send_text(f"From {sender_id}: {content}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    asyncio.create_task(receive_from_chat_service())


# TODO: add correct error-handling
@router.post("/conversation")
async def create_chat_conversation(
    request_data: ConversationBase,
    # other_user_id: UUID,
    # token: str = Depends(authenticator.authenticate)
):
    user_id = "00cebe39-9159-500a-a4d3-efb9932ec33a"
    other_user_id = request_data.other_user_id
    # TODO: check this syntax
    async with aiohttp.ClientSession() as session:
        url = CHAT_SERVICE_CREATE_CONVERSATION_URL_LOCAL
        payload = {"user_first_id": str(user_id), "user_second_id": str(other_user_id)}
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=await response.text())
            conversation_data = await response.json()
    return conversation_data


@router.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: UUID,
    token: str = Depends(authenticator.authenticate),
):
    user_id = token["sub"]
    await manager.connect(websocket, user_id)

    await connect_to_chat_service(conversation_id)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            recipient_id = message.get("recipient_id")
            content = message.get("content")

            if not recipient_id or not content:
                await websocket.send_text("Invalid message format.")
                continue

            await chat_service_ws.send_json(
                {
                    "action": "send_message",
                    "data": {
                        "sender_id": user_id,
                        "recipient_id": str(recipient_id),
                        "content": content,
                    },
                }
            )
            await websocket.send_text("Message sent successfully.")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
