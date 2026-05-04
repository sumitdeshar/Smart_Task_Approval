from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 

from configs.db import get_session
from models.user_model import User
from utils.token import token_utils
from utils.token.blacklist_token import is_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    payload = token_utils.decode_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def verify_access_token(
    token_str: str
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = token_utils.verify_token(token_str, credentials_exception)
    print('user id form token auth:',user_id)
    return user_id


def verify_refresh_token(token: str):
    payload = token_utils.decode_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    jti = payload.get("jti")
    if jti:
        if is_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")
    return payload