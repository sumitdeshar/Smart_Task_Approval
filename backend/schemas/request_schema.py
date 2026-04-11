from sqlmodel import SQLModel
from typing import Optional

class RequestBase(SQLModel):
    token: dict
    data: Optional[dict] = None
    
class LogoutRequest(SQLModel):
    access_token: Optional[str] = None
