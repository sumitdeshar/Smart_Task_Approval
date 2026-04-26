from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship

def utcnow(): return datetime.now(timezone.utc)
def new_uuid(): return str(uuid4())

class UserRoleLink(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)

class RoleName(str, Enum):
    ADMIN    = "admin"
    MANAGER  = "manager"
    EMPLOYEE = "employee"

class LeaveStatus(str, Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: RoleName = Field(unique=True, index=True)
    description: Optional[str] = None
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

class User(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)
    leaves: List["Leave"] = Relationship(back_populates="user")

class Leave(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None
    status: LeaveStatus = Field(default=LeaveStatus.PENDING)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    user: User = Relationship(back_populates="leaves")

class UserSession(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    started_at: datetime = Field(default_factory=utcnow)
    ended_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    logs: List["APILog"] = Relationship(back_populates="session")

class APILog(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)
    session_id: Optional[str] = Field(foreign_key="usersession.id", default=None)
    user_id: Optional[str] = Field(default=None, index=True)
    method: str
    path: str
    status_code: int
    duration_ms: int
    timestamp: datetime = Field(default_factory=utcnow)
    session: Optional[UserSession] = Relationship(back_populates="logs")