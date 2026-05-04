from fastapi import APIRouter, Depends, HTTPException, Request 
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.user_model import RoleName, User
from schemas.user_schema import UserUpdate
from utils.roles import require_roles
from utils.token.token_auth import get_current_user, oauth2_scheme

user_router = APIRouter()

@user_router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔐 Allow admin/manager OR self
    if current_user.role not in [RoleName.ADMIN, RoleName.MANAGER]:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

    return user

@user_router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔐 Authorization
    is_admin_or_manager = current_user.role in [RoleName.ADMIN, RoleName.MANAGER]

    if not is_admin_or_manager and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 🔐 Restrict role change (only admin can change roles)
    if request.role is not None:
        if current_user.role != RoleName.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can change roles"
            )
        user.role = request.role

    # Update other fields
    if request.name is not None:
        user.name = request.name

    if request.email is not None:
        user.email = request.email

    await session.commit()
    await session.refresh(user)

    return user

@user_router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(
        require_roles([RoleName.ADMIN, RoleName.MANAGER])
    ),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    await session.delete(user)
    await session.commit()

    return {"msg": "User deleted successfully"}
