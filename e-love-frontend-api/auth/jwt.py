import os
from jose import jwt, JWTError
from fastapi import HTTPException, status


class JWTService:
    """
    Системный сервис для работы с JWT-токенами. Предоставляет методы для создания и верификации токенов.
    vars:
        supabase_secret: Секретный ключ для создания и верификации токенов
    methods:
        verify_token - проверка токена
    """

    def __init__(self):
        self.supabase_secret = os.getenv("SUPABASE_JWT_SECRET")

    def verify_token(self, token: str) -> dict:
        """
        Метод сервиса JWTService, который проверяет Supabase токен на валидность.
        params: token - токен
        return: payload - полезная нагрузка токена
        raises: HTTPException - если токен недействителен
        """
        try:
            payload = jwt.decode(
                token,
                key=self.supabase_secret,
                algorithms=["HS256"],
            )
            return payload
        except JWTError as e:
            raise Exception(f"Token error: {e}")
