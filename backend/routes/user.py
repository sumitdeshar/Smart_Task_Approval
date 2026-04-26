from fastapi import APIRouter, Depends, HTTPException, Request 
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.user_model import User
from utils.token.token_auth import oauth2_scheme

user_router = APIRouter()

@user_router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.delete("/delete/user")
async def delete_user(
    request: Request,
    token_str: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
):
    user_id = 1
    body = request.cookies
    print(body)
    # user_id = body.get("user_id")
    
    # result = await session.execute(select(User).where(User.id == user_id))
    # user = result.scalars().one_or_none()

    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # await session.delete(user)
    # await session.commit()
    # return {"msg": f"User {user.email} deleted successfully"}
    return user_id

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
