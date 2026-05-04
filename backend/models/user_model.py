from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4
from enum import Enum
from sqlalchemy import Column, DateTime

from sqlmodel import Field, SQLModel, Relationship


# ✅ timezone-aware datetime
def utcnow():
    return datetime.now(timezone.utc)


def new_uuid():
    return str(uuid4())


# 🎭 Role Enum
class RoleName(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


# 📄 Leave status
class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# 👤 User Table
class User(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    name: str
    email: str = Field(unique=True, index=True)
    password: str
    role: RoleName = Field(default=RoleName.EMPLOYEE)

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=utcnow)
    )

    leaves: List["Leave"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


# 📅 Leave Table
class Leave(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(foreign_key="user.id")

    start_date: datetime
    end_date: datetime

    reason: Optional[str] = None

    status: LeaveStatus = Field(default=LeaveStatus.PENDING)

    created_at: datetime = Field(default_factory=utcnow)

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column_kwargs={"onupdate": utcnow}
    )

    user: User = Relationship(back_populates="leaves")


# 🧾 Session tracking
class UserSession(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    user_id: str = Field(foreign_key="user.id", index=True)

    started_at: datetime = Field(default_factory=utcnow)
    ended_at: Optional[datetime] = None

    ip_address: Optional[str] = None

    logs: List["APILog"] = Relationship(back_populates="session")


# 📊 API logs
class APILog(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    session_id: Optional[str] = Field(
        foreign_key="usersession.id",
        default=None
    )

    user_id: Optional[str] = Field(default=None, index=True)

    method: str
    path: str
    status_code: int
    duration_ms: int

    timestamp: datetime = Field(default_factory=utcnow)

    session: Optional[UserSession] = Relationship(back_populates="logs")