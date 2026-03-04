from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_session
from models.model import User

test = APIRouter()

@test.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@test.post("/users")
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user