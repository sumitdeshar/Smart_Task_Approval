from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import IntegrityError
from sqlmodel import or_, select
from uuid import uuid4
from jose import JWTError

from configs.db import get_session
from models.user_model import User
from schemas.request_schema import LogoutRequest
from schemas.user_schema import UserCreate, UserLogin, UserResponseRegister

from utils.hashing import Hash
from utils import token_utils as token
from utils.token_auth import verify_access_token, oauth2_scheme
from utils import blacklist_token

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


        access_token = token.create_access_token(data={"sub": user.id})
        refresh_token = token.create_refresh_token(data={"sub": user.id})
        # print(f'access_token', access_token)   
        # print(f'resfresh_token', refresh_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
            "user": UserResponseRegister.from_orm(user)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@auth.post("/logout")
async def logout(
    request: LogoutRequest,
    token_str: str = Depends(oauth2_scheme)
):

    payload = token.decode_token(token_str)
    jti = payload.get("jti")
    
    if not jti:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    
    blacklist_token.blacklist_token(jti)

    if request.access_token:
        try:
            access_payload = token.decode_token(request.access_token)
            access_jti = access_payload.get("jti")
            if access_jti:
                blacklist_token.blacklist_token(access_jti)
        except JWTError:
            pass  # Ignore invalid refresh token

    return {"msg": "Logged out successfully"}


@auth.delete("/user/{user_id}")
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"msg": f"User {user.email} deleted successfully"}

