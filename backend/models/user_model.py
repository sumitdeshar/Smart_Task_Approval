from datetime import datetime, date
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

# Association table for User <-> Role many-to-many
class UserRoleLink(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)

# Role table
class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., Admin, Manager, Employee
    description: Optional[str] = None

    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

# User table
class User(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)
    leaves: List["Leave"] = Relationship(back_populates="user")  
    
class Leave(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")  # which user applied
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: str = Field(default="Pending")  # Pending, Approved, Rejected
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship back to user
    user: User = Relationship(back_populates="leaves")