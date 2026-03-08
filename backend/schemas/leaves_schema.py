from sqlmodel import SQLModel
from datetime import date
from typing import Optional


class LeaveBase(SQLModel):
    start_date: date
    end_date: date
    reason: str

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(SQLModel):
    status: str
    manager_comment: Optional[str] = None

class LeaveRead(LeaveBase):
    id: int
    employee_id: int
    status: str