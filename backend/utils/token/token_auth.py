from fastapi import HTTPException, status, Header, Depends, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from utils.token import token_utils
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_current_user(authorization: Optional[str] = Header(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise credentials_exception

    token_str = authorization.split(" ")[1]
    user_id = token_utils.verify_token(token_str, credentials_exception)
    return user_id

def verify_access_token(
    request: Request,
    token_str: str = Depends(oauth2_scheme)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = token_utils.verify_token(token_str, credentials_exception)
    print('user id form token auth:',user_id)
    return user_id

def verify_refresh_token(
    refresh_token: str = Cookie(None)   # browser sends this automatically
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided"
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    user_id = token_utils.verify_token(refresh_token, credentials_exception)
    return user_id