import asyncio
import json
import os
from uuid import UUID

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from auth.security import authenticator
from configuration.database import get_db_session
from core.schemas.chat.conversation.conversation_schema import ConversationBase
from utils.chat.connect_to_chat_service import connect_to_chat_service
from utils.chat.listen_chat_service import listen_chat_service

router = APIRouter()

# TODO: make a condition here where we want to pick a variable depends on prod/local env (in the future)
CHAT_SERVICE_CREATE_CONVERSATION_URL_LOCAL = os.getenv("CHAT_SERVICE_CREATE_CONVERSATION_URL_LOCAL")
CHAT_SERVICE_CONNECT_URL_LOCAL = os.getenv("CHAT_SERVICE_CONNECT_URL_LOCAL")
CHAT_SERVICE_AUTH_TOKEN = os.getenv("CHAT_SERVICE_AUTH_TOKEN")

chat_service_ws = None


# TODO: add correct error-handling
@router.post("conversation")
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


# TODO: add auth0 integration (check user_token)
@router.websocket("{conversation_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    conversation_id: UUID,
    # token: str = Depends(authenticator.authenticate),
):
    """
    WebSocket endpoint that proxies chat messages between Frontend and Chat-Microservice.
    Requires a valid token and a conversation_id in query params.
    """

    # user_payload = token
    # user_id = user_payload["sub"]

    # Accept client-connection

    await websocket.accept()

    chat_service_ws = await connect_to_chat_service(str(conversation_id))

    asyncio.create_task(listen_chat_service(chat_service_ws, websocket))

    try:
        while True:
            client_msg = await websocket.receive_json()
            await chat_service_ws.send_json(client_msg)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        pass
    finally:
        await chat_service_ws.close()
