# app/auth/jwt.py
# WARN: ChatGPT-generated code!

import json
from typing import Any, Dict
from urllib.request import urlopen

from jose import jwt

from auth.config import auth_settings


class JWTService:

    def __init__(self):
        """
        Конструктор сервиса JWTService, который возвращает Access Bearer token JWT-формата,
        который нужно использовать для доступа к нашим эндпоинтам.

        - **auth0_domain** - Домен нашего auth0-tenant;
        - **audience** - Полная ссылка на наш auth0-API;
        - **jwks_url** - ссылка для получения Access Token от Auth0.
        """
        self.auth0_domain = auth_settings.auth0_domain
        self.audience = auth_settings.auth0_api_audience
        self.jwks_url = f"https://{self.auth0_domain}/.well-known/jwks.json"
        self.jwks = self._get_jwks()

    def _get_jwks(self) -> Dict[str, Any]:
        """
        Метод, который получает access-token из нашего auth0-tenant;
        """
        with urlopen(self.jwks_url) as response:
            return json.loads(response.read())

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Метод, который проверяет подлинность нашего access-token.
        Я пока сам не понимаю, как он работает.
        """
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in self.jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=self.audience,
                    issuer=f"https://{self.auth0_domain}/",
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise Exception("Token has expired")
            except jwt.JWTClaimsError:
                raise Exception("Incorrect claims, please check the audience and issuer")
            except Exception as e:
                raise Exception(f"Unable to parse token: {e}")
        else:
            raise Exception("Unable to find appropriate key")
