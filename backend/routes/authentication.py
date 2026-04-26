from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import IntegrityError
from sqlmodel import or_, select
from uuid import uuid4
from jose import JWTError

from configs.db import get_session
from models.user_model import User
from schemas.request_schema import LogoutRequest
from schemas.user_schema import UserCreate, UserResponseRegister

from utils.hashing import Hash
from utils.token import token_utils as token
from utils.token.token_auth import oauth2_scheme, verify_refresh_token

auth = APIRouter(prefix="/auth", tags=["Authentication"])
    
@auth.post("/register" )
async def register(request: UserCreate, session: AsyncSession = Depends(get_session)):
    data = {}
    
    new_user = User(
        id=str(uuid4()),
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
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

    
@auth.post("/login" )
async def login(
    response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    data = {}
    try:
        res = await session.execute(
            select(User).where(
                    User.email == request.username,
            )
        )
        user = res.scalars().one_or_none()

        if not user or not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        data["user"] = UserResponseRegister.from_orm(user)


        access_token = token.create_access_token(data={"sub": user.id, "role": user.role})
        refresh_token = token.create_refresh_token(data={"sub": user.id})
        # print(f'access_token', access_token)   
        # print(f'resfresh_token', refresh_token)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,       # JS cannot read this
            secure=True,         # HTTPS only (set False for local dev)
            samesite="lax",      # CSRF protection
            max_age=60 * 60 * 24 * 7  # 7 days in seconds
        )
            
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponseRegister.from_orm(user)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@auth.post("/refresh")
async def refresh(
    response: Response,
    user_id: int = Depends(verify_refresh_token)
):
    new_access_token = token.create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token}


@auth.post("/logout")
async def logout(
    request: LogoutRequest,
    token_str: str = Depends(oauth2_scheme)
):
    user_id = token.verify_token(token_str, credentials_exception= "sad")
    print(user_id)
    return {"msg": "Logged out successfully"}
