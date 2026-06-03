from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


# =========================================================
# HELPERS
# =========================================================

def utcnow():
    return datetime.now(timezone.utc)


def new_uuid():
    return str(uuid4())


# =========================================================
# ENUMS
# =========================================================

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# =========================================================
# USER
# =========================================================

class User(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    name: str
    email: str = Field(unique=True, index=True)
    password: str

    role: UserRole = Field(default=UserRole.USER)

    is_active: bool = Field(default=True)

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=utcnow
        )
    )

    # Relationships
    created_tasks: List["Task"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "[Task.created_by]"}
    )

    assigned_tasks: List["TaskAssignment"] = Relationship(
        back_populates="assignee",
        sa_relationship_kwargs={"foreign_keys": "[TaskAssignment.assigned_to]"}
    )

    created_assignments: List["TaskAssignment"] = Relationship(
        back_populates="assigner",
        sa_relationship_kwargs={"foreign_keys": "[TaskAssignment.assigned_by]"}
    )

    comments: List["TaskComment"] = Relationship(
        back_populates="user"
    )

    resolutions: List["TaskResolution"] = Relationship(
        back_populates="resolver"
    )

    activities: List["TaskActivity"] = Relationship(
        back_populates="user"
    )

    sessions: List["UserSession"] = Relationship(
        back_populates="user"
    )

    api_logs: List["APILog"] = Relationship(
        back_populates="user"
    )


# =========================================================
# TASK
# =========================================================

class Task(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    title: str
    description: Optional[str] = None

    status: TaskStatus = Field(default=TaskStatus.OPEN)

    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM
    )

    created_by: str = Field(
        foreign_key="user.id"
    )

    deadline: Optional[datetime] = Field(
    default=None,
    sa_column=Column(DateTime(timezone=True))
)
    # With sa_column:

    # deadline: datetime = Field(
    #     sa_column=Column(DateTime(timezone=True))
    # )

    # You explicitly tell SQLModel:
    # Create this column as a timezone-aware datetime.

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=utcnow
        )
    )

    # Relationships
    creator: Optional[User] = Relationship(
        back_populates="created_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.created_by]"}
    )

    assignments: List["TaskAssignment"] = Relationship(
        back_populates="task"
    )

    comments: List["TaskComment"] = Relationship(
        back_populates="task"
    )

    resolutions: List["TaskResolution"] = Relationship(
        back_populates="task"
    )

    activities: List["TaskActivity"] = Relationship(
        back_populates="task"
    )


# =========================================================
# TASK ASSIGNMENTS
# =========================================================

class TaskAssignment(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    task_id: str = Field(
        foreign_key="task.id"
    )

    assigned_to: str = Field(
        foreign_key="user.id"
    )

    assigned_by: str = Field(
        foreign_key="user.id"
    )

    assigned_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    # Relationships
    task: Optional[Task] = Relationship(
        back_populates="assignments"
    )

    assignee: Optional[User] = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={"foreign_keys": "[TaskAssignment.assigned_to]"}
    )

    assigner: Optional[User] = Relationship(
        back_populates="created_assignments",
        sa_relationship_kwargs={"foreign_keys": "[TaskAssignment.assigned_by]"}
    )


# =========================================================
# TASK COMMENTS / DISCUSSIONS
# =========================================================

class TaskComment(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    task_id: str = Field(
        foreign_key="task.id"
    )

    user_id: str = Field(
        foreign_key="user.id"
    )

    subject: str
    message: str

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=utcnow
        )
    )

    # Relationships
    task: Optional[Task] = Relationship(
        back_populates="comments"
    )

    user: Optional[User] = Relationship(
        back_populates="comments"
    )


# =========================================================
# TASK RESOLUTION / FINAL SOLUTION
# =========================================================

class TaskResolution(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    task_id: str = Field(
        foreign_key="task.id"
    )

    resolved_by: str = Field(
        foreign_key="user.id"
    )

    summary: str

    root_cause: Optional[str] = None

    solution: Optional[str] = None

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    # Relationships
    task: Optional[Task] = Relationship(
        back_populates="resolutions"
    )

    resolver: Optional[User] = Relationship(
        back_populates="resolutions",
        sa_relationship_kwargs={"foreign_keys": "[TaskResolution.resolved_by]"}
    )


# =========================================================
# TASK ACTIVITY LOG
# =========================================================

class TaskActivity(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    task_id: str = Field(
        foreign_key="task.id"
    )

    user_id: Optional[str] = Field(
        foreign_key="user.id",
        default=None
    )

    action: str
    details: Optional[str] = None

    created_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    # Relationships
    task: Optional[Task] = Relationship(
        back_populates="activities"
    )

    user: Optional[User] = Relationship(
        back_populates="activities",
        sa_relationship_kwargs={"foreign_keys": "[TaskActivity.user_id]"}
    )


# =========================================================
# USER SESSION TRACKING
# =========================================================

class UserSession(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    user_id: str = Field(
        foreign_key="user.id",
        index=True
    )

    started_at: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    ended_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True))
    )

    ip_address: Optional[str] = None

    user_agent: Optional[str] = None

    # Relationships
    user: Optional[User] = Relationship(
        back_populates="sessions"
    )

    logs: List["APILog"] = Relationship(
        back_populates="session"
    )


# =========================================================
# API REQUEST LOGS
# =========================================================

class APILog(SQLModel, table=True):
    id: str = Field(default_factory=new_uuid, primary_key=True)

    session_id: Optional[str] = Field(
        foreign_key="usersession.id",
        default=None
    )

    user_id: Optional[str] = Field(
        foreign_key="user.id",
        default=None,
        index=True
    )

    method: str
    path: str
    status_code: int

    duration_ms: int

    timestamp: datetime = Field(
        default_factory=utcnow,
        sa_column=Column(DateTime(timezone=True))
    )

    # Relationships
    session: Optional[UserSession] = Relationship(
        back_populates="logs"
    )

    user: Optional[User] = Relationship(
        back_populates="api_logs"
    )