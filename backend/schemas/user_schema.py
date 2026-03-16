from sqlmodel import SQLModel
from typing import Optional

class UserBase(SQLModel):
    email: str
    name: str
    
class UserCreate(UserBase):
    password: str
    
class UserLogin(UserCreate):
    name : Optional[str]
    
class UserResponseRegister(UserBase):
    id: str

    class Config:
        from_attributes = True
