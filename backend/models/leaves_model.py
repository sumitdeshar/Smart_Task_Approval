from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date


class LeaveRequest(SQLModel, table=True):
    __tablename__ = "leave_requests" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(foreign_key="users.id")

    start_date: date
    end_date: date

    reason: str

    status: str = Field(default="pending")  
    # pending | approved | rejected

    manager_comment: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)