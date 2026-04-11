from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.user_model import User

user_router = APIRouter()

@user_router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

# @user_router.get("/user/{user_id}")
# async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
#     return user
    

#SQLModel tips
# SQLModel internally automatically does scalars().

# So: no scalars are needed

# exec() = execute() + scalars()

# Available Methods:
# scalar() - First row, first column
# scalar_one() - First row, first column, raises if no results
# scalar_one_or_none() - Like scalar_one() but returns None if no results
# first() - Returns first row or None
# one() - Returns single row, raises if 0 or >1 rows
# one_or_none() - Returns single row or None, raises if >1 rows
# all() - Returns all rows as list
