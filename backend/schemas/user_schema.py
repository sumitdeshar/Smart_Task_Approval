from sqlmodel import SQLModel

class UserBase(SQLModel):
    email: str
    full_name: str
    
class UserCreate(UserBase):
    password: str
    
class UserRead(UserBase):
    id: str
    roles: str
