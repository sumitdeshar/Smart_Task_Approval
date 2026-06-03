from fastapi import Depends, HTTPException
from models.models import UserRole, User
from utils.token.token_auth import get_current_user


def check_roles(user: User, allowed_roles: list[UserRole]):
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

def check_self(user: User, user_id: str):
    if str(user.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
        
def check_self_or_roles(
    user: User,
    resource_user_id: str,
    allowed_roles: list[UserRole]
):
    if user.role in allowed_roles:
        return

    if str(user.id) == resource_user_id:
        return

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


# reusable dependencies
def AdminOnly(current_user: User = Depends(get_current_user)):
    check_roles(current_user, [UserRole.ADMIN])
    return current_user

def AdminOrManager(current_user: User = Depends(get_current_user)):
    check_roles(current_user, [UserRole.ADMIN, UserRole.MANAGER])
    return current_user

def SelfOrAdmin(user_id: str):
    def dependency(current_user: User = Depends(get_current_user)):
        check_self_or_roles(
            user=current_user,
            resource_user_id=user_id,
            allowed_roles=[UserRole.ADMIN]
        )
        return current_user

    return dependency


