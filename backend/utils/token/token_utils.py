from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from uuid import uuid4
import os

from .blacklist_token import is_blacklisted

SECRET_KEY = os.getenv("SECRET_KEY", "your-random-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": str(uuid4())
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid4())
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_token(token: str, credentials_exception):
    try:
        if not token:
            raise credentials_exception

        payload = decode_token(token)
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=400, detail="Invalid token payload")
    
        if is_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        return user_id

    except JWTError:
        raise credentials_exception
