from fastapi import APIRouter, Depends, HTTPException, Request 
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.models import User, UserRole
from schemas.user_schema import UserUpdate
from utils.roles_dependencies import (
    AdminOnly,
    AdminOrManager,
    SelfOrAdmin
)

user_router = APIRouter()

@user_router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    current_user: User = Depends(SelfOrAdmin),
    
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@user_router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdate,
    current_user: User = Depends(SelfOrAdmin),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
    current_user: User = Depends(AdminOrManager),
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
