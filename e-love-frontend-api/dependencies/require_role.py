from fastapi import Depends, HTTPException, status
from core.db.models.users.users import User
from dependencies.get_current_user import get_current_user


async def require_role(role_name: str):
    """
    Возвращает функцию-зависимость, которая примет User (из get_current_user)
    и проверит, есть ли у него нужная роль.
    """

    async def checker(current_user: User = Depends(get_current_user)):
        roles_names = [r.name for r in current_user.roles]
        if role_name not in roles_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Role '{role_name}' is required."
            )
        return current_user

    return checker
