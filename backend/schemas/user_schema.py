from sqlmodel import SQLModel
from typing import Optional, List

from models.models import UserRole

class UserBase(SQLModel):
    email: str
    name: str
    role: Optional[UserRole] = None
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
    role: Optional[UserRole] = None
    
class UserMakeAdmin(SQLModel):
        role: Optional[UserRole] = UserRole.USER
