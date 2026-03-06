from fastapi import APIRouter, Depends, HTTPException, status

from utils.hashing import Hash
from utils import token_utils
from models.user import User
from config.db import get_session

from sqlmodel import or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserOut)
async def create_user(request: UserIn, session: AsyncSession = Depends(get_session)):
    # Check if email exists
    existing_user = await session.exec(
        select(User).where(User.email == request.email)
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        id=str(uuid.uuid4()),
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    await session.close()
    return new_user


@router.post("/login")
async def login(request: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        res = await session.execute(
            select(User).where(
                or_(
                    User.email == request.username_or_email,
                    User.name == request.username_or_email
                    )
                )
            )
        user =res.scalar_one()
        print("User fetched:", user)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
        if not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = token_utils.create_access_token(data={"sub": user.id})
        print(f'access_token', access_token)   
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )
    finally:
        await session.close()
        
