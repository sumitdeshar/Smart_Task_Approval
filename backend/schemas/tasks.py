from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
from models.models import TaskPriority, TaskStatus


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    deadline: Optional[datetime] = None
    