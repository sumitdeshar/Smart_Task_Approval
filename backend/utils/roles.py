from fastapi import Depends, HTTPException
from models.user_model import RoleName, User
from utils.token.token_auth import get_current_user


def require_roles(allowed_roles: list[RoleName]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_self_or_roles(allowed_roles: list[RoleName]):
    async def checker(
        user_id: str,
        current_user: User = Depends(require_roles(allowed_roles))
    ):
        # If already admin/manager → allowed
        if current_user.role in allowed_roles:
            return current_user

        # Otherwise must be self
        if current_user.id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        return current_user
    return checker

