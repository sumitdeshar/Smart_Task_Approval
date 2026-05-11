from fastapi import Depends, HTTPException
from models.models import UserRole, User
from utils.token.token_auth import get_current_user


# This Pattern Is Called
# Higher-order function
# Dependency factory
# Closure

# The inner function "remembers" allowed_roles.

# That memory behavior is called a closure.

def require_roles(allowed_roles: list[UserRole]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_self():

    async def checker(
        user_id: str,
        current_user: User = Depends(get_current_user)
    ):

        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        return current_user

    return checker

def require_self_or_roles(
    allowed_roles: list[UserRole]
):

    async def checker(
        user_id: str,
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role in allowed_roles:
            return current_user

        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        return current_user

    return checker


# reusable dependencies
AdminOnly = Depends(
    require_roles([UserRole.ADMIN])
)

AdminOrManager = Depends(
    require_roles([
        UserRole.ADMIN,
        UserRole.MANAGER
    ])
)

SelfOrAdmin = Depends(
    require_self_or_roles([
        UserRole.ADMIN
    ])
)

