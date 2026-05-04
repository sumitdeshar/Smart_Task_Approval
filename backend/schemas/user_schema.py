from sqlmodel import SQLModel
from typing import Optional, List

from models.user_model import RoleName

class UserBase(SQLModel):
    email: str
    name: str
    class Config:
        from_attributes = True
    
class UserCreate(UserBase):
    password: str
    
class UserLogin(UserCreate):
    name : Optional[str]
    
class UserResponseRegister(UserBase):
    id: str

    class Config:
        from_attributes = True

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[RoleName] = None
