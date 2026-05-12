from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import IntegrityError
from sqlmodel import or_, select

from configs.db import get_session
from models.models import User
from schemas.request_schema import LogoutRequest
from schemas.user_schema import UserCreate, UserResponseRegister

from utils.hashing import Hash
from utils.token import token_utils as token
from utils.token.blacklist_token import is_blacklisted, add_token_to_blacklist
from utils.token.token_auth import oauth2_scheme, verify_refresh_token, verify_access_token

auth = APIRouter(prefix="/auth", tags=["Authentication"])
    
@auth.post("/register" )
async def register(request: UserCreate, session: AsyncSession = Depends(get_session)):
    data = {}
    
    new_user = User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
        role= request.role,
    )
    
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError:
        await session.rollback()
        data["msg"] = "Email already used"
        return data
    data['msg'] = "User Created Successfully"
    return data

    
from sqlalchemy import or_
from fastapi import HTTPException, status

@auth.post("/login")
async def login(
    response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    identifier = request.username

    if not identifier:
        raise HTTPException(status_code=400, detail="Username/email required")

    res = await session.execute(
        select(User).where(
            or_(
                User.email == identifier, # pyright: ignore[reportArgumentType]
                User.name == identifier # pyright: ignore[reportArgumentType]
            )
        )
    )

    user = res.scalars().one_or_none()


    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )

    try:
        access_token = token.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        refresh_token = token.create_refresh_token(
            data={"sub": str(user.id)}
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Token generation failed"
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponseRegister.model_validate(user)
    }

@auth.get("/check-cookie")
async def check_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return {"message": "No cookie received"}

    return {
        "message": "Cookie received",
        "token": refresh_token
    }

@auth.post("/refresh")
async def refresh(
    response: Response,
    payload: dict = Depends(verify_refresh_token),
    session: AsyncSession = Depends(get_session)
):
    user_id = payload.get("sub")
    
    jti = payload.get("jti")

    if not user_id or not jti:
        raise HTTPException(status_code=401, detail="Invalid token")

    res = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = res.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    add_token_to_blacklist(jti)

    new_access_token = token.create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    new_refresh_token = token.create_refresh_token(
        data={"sub": str(user.id)}
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }

@auth.post("/logout")
async def logout(
    request: LogoutRequest,
    token_str: str = Depends(oauth2_scheme)
):
    user_id = verify_access_token(token_str)
    print(user_id)
    return {"msg": "Logged out successfully"}
