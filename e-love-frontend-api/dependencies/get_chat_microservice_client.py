# fe_api/dependencies.py
import os

from api.clients.chat_microservice_client import ChatMicroserviceClient


def get_chat_microservice_client():
    base_url = os.getenv("CHAT_MICROSERVICE_BASE_URL")
    return ChatMicroserviceClient(base_url)
