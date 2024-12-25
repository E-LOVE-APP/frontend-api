# app/auth/security.py
# WARN: ChatGPT generated code!

from typing import Callable, List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import auth_settings
from .jwt import JWTService

jwt_service = JWTService()
security = HTTPBearer()


# TODO: rename to AuthenticatorService?
class Authenticator:
    """
    Класс для аутентификации пользователей. Предоставляет методы для аутентификации и проверки ролей.
    vars:
        jwt_service: Сервис для работы с JWT-токенами
    methods:
        authenticate - аутентификация пользователя
        require_role - проверка роли пользователя
    """

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    def authenticate(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """
        Аутентифицирует пользователя по токену.

        :param credentials: Креденшелы из заголовка Authorization
        :return: Полезная нагрузка токена
        :raises HTTPException: Если токен недействителен
        """
        token = credentials.credentials
        try:
            payload = self.jwt_service.verify_token(token)
            return payload
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def require_role(self, role: str) -> Callable:
        """
        Проверяет, имеет ли пользователь необходимую роль.

        :param role: Требуемая роль
        :return: Функция зависимости
        """

        def role_checker(payload: dict = Depends(self.authenticate)) -> dict:
            if "permissions" in payload and role in payload["permissions"]:
                return payload
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(f"Forbidden: insufficient permissions. Required roles list: ", role),
            )

        return role_checker


authenticator = Authenticator(jwt_service)
