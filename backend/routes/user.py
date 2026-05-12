from fastapi import APIRouter, Depends, HTTPException, Request 
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.models import User, UserRole
from schemas.user_schema import UserUpdate, UserMakeAdmin
from utils.roles_dependencies import (
    AdminOnly,
    AdminOrManager,
    SelfOrAdmin
)

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("/get-all-users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found!")
    return users

@user_router.get("/get/{user_id}")
async def get_user(
    user_id: str,
    current_user: User = SelfOrAdmin,
    
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@user_router.put("/update/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdate,
    current_user: User = SelfOrAdmin,
    session: AsyncSession = Depends(get_session)
):
    data ={}
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
    data["msg"] = "User updated successfully"
    data["user"] = user
    return data

@user_router.delete("/delete/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = AdminOrManager,
    session: AsyncSession = Depends(get_session)
):
    data = {}
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
    
    data["msg"] = "User deleted successfully"
    return data


@user_router.post("/make-admin/{user_id}")
async def make_admin(
    user_id: str,
    request: UserUpdate,
    current_user: User = AdminOnly,
    
    session: AsyncSession = Depends(get_session)
):
    data= {}
    result = await session.execute(
        select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.role is not None:
        if request.role == user.role:
            raise HTTPException(status_code=402, detail=f"User role is already ${request.role}")
        else:
            user.role = request.role
    
        await session.commit()
    await session.refresh(user)
    
    data["msg"] = "User role successfully changed."
    data["user"] = user
    return data