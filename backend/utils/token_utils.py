from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from uuid import uuid4
import os

#use this to generate secrect key on your terminal
# import secrets
# SECRET_KEY = secrets.token_hex(32)
# print('secrect key:', SECRET_KEY)

SECRET_KEY = os.getenv("SECRET_KEY", "aa") # second parameter is random string to make it so that secret key is never null
ALGORITHM = os.getenv("ALGORITHM", "aa")

# ACCESS_TOKEN_EXPIRE_MINUTES = 7
# ACCESS_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

blacklist = set()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": str(uuid4())
                      })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

def is_token_blacklisted(jti: str):
    return jti in blacklist


def verify_token(token: str, credentials_exception):
    try:
        if not token:
            raise credentials_exception

        payload = decode_token(token)

        jti = payload.get("jti")

        if jti in blacklist:
            raise HTTPException(
                status_code=401,
                detail="Token has been revoked"
            )

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


def blacklist_token(jti: str):
    if not jti:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    if is_token_blacklisted(jti):
        return {'msg': 'Token already in blacklist.'}
    blacklist.add(jti)
    return {'msg': "Token blacklisted Done."}




