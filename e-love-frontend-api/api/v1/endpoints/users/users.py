# Users controller
# pylint: disable-all
# type: ignore
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


# Это обычный тестовый рут чтобы проверить что у тебя работает роутер (проверить что руты добавляются можешь просмотрев логи в fe-api контейнере)
@router.post("/register", response_model=None, status_code=status.HTTP_201_CREATED)
async def register_user(db: None):
    """
    Регистрирует нового пользователя.

    - **first_name**: Имя пользователя.
    - **last_name**: Фамилия пользователя.
    - **email**: Электронная почта пользователя.
    - **password**: Пароль пользователя.
    """
    pass


# Тут будут методы котнроллера и руты, которые ты можешь использовать благодаря router. Для хорошей декомпозиции, все эти руты будут извлекаться в api/v1/router/router.py ,
# для того, чтобы в main.py мы могли внедрить один общий роутер.
