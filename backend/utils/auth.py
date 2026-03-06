from fastapi import HTTPException, status, Header
from typing import Optional
from utils import token_utils


def get_current_user(authorization: Optional[str] = Header(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if authorization is not None:
        user_id = token_utils.verify_token(authorization, credentials_exception)
    else:
        raise credentials_exception
    return user_id