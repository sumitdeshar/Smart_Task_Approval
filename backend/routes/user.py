from models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from config.db import get_session

user_router = APIRouter()

@user_router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.get("/users/{user_id}")
async def get_user_by_id(user_id: int, sessions: AsyncSession = Depends(get_session)):
    result = await sessions.execute(select.where(User.id == user_id))
    user = result.scalars().all()
    print(user)
    if user is None:
        return {"msg": "user by this id is not present"}
    return user
    

@user_router.post("/users")
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    if user.roles is None:
        user.roles = "user"
    if user.email is None:
        user.email = f"{user.name.lower()}@example.com"
    if user.name is None:
        user.name = "Unnamed User"
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# Available Methods:
# scalar() - First row, first column
# scalar_one() - First row, first column, raises if no results
# scalar_one_or_none() - Like scalar_one() but returns None if no results
# first() - Returns first row or None
# one() - Returns single row, raises if 0 or >1 rows
# one_or_none() - Returns single row or None, raises if >1 rows
# all() - Returns all rows as list