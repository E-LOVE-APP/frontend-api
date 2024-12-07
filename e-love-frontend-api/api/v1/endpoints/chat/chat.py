import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from configuration.database import get_db_session
from api.conn_manager.conn_manager import ConnectionManager
from auth.security import authenticator

import aiohttp

router = APIRouter()

manager = ConnectionManager()

# TODO: refactor!!! ADD THIS TO ENV!

# URL для Chat-Microservice WebSocket сервера
CHAT_SERVICE_WS_URL = "ws://chat-service-api:8001/ws/chat"

# Секретный токен для аутентификации между микросервисами
CHAT_SERVICE_AUTH_TOKEN = "fe-api-secret-token"

chat_service_ws = None
