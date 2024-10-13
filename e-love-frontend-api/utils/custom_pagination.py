import base64
import json
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class Paginator(Generic[T]):
    def __init__(self, limit: int = 10):
        self.limit = limit

    def encode_token(self, last_created_at: str, last_id: str) -> str:
        token_dict = {"created_at": last_created_at, "id": last_id}
        token_str = json.dumps(token_dict)
        token_bytes = token_str.encode("utf-8")
        encoded_token = base64.urlsafe_b64encode(token_bytes).decode("utf-8")
        return encoded_token

    def decode_token(self, token: str) -> Dict[str, str]:
        try:
            token_bytes = base64.urlsafe_b64decode(token.encode("utf-8"))
            token_str = token_bytes.decode("utf-8")
            token_dict = json.loads(token_str)
            return token_dict
        except Exception:
            raise ValueError("Invalid token")

    def get_response(
        self,
        model_name: str,
        items: List[T],
        has_next: bool,
        next_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            model_name: items,
            "hasNext": has_next,
            "nextToken": next_token,
        }
