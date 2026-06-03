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
    
    
class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    
    