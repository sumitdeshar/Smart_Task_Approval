from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from sqlmodel import or_, select

from configs.db import get_session
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin, UserResponseRegister
from utils.hashing import Hash
from utils import token_utils as token

auth = APIRouter(prefix="/auth", tags=["Authentication"])
    
@auth.post("/register", response_model=UserResponseRegister)
async def register(request: UserCreate, session: AsyncSession = Depends(get_session)):
    
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
        return {"msg": "Email already used"}
    return new_user

@auth.post("/login" )
async def login(request: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        res = await session.execute(
            select(User).where(
                    User.email == request.email,
            )
        )
        user = res.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Give correct username or password"
            )
        
        if not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        access_token = token.create_access_token(data={"sub": user.id})
        print(f'access_token', access_token)   
        return {"token":{"access_token": access_token, "token_type": "bearer"},
                "data": UserResponseRegister.from_orm(user)}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
