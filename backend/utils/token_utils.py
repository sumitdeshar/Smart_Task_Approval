from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

#use this to generate secrect key on your terminal
# import secrets
# SECRET_KEY = secrets.token_hex(32)
# print('secrect key:', SECRET_KEY)

SECRET_KEY = os.getenv("SECRET_KEY", "aa") # second parameter is random string to make it so that secret key is never null
ALGORITHM = os.getenv("ALGORITHM", "aa")
# ACCESS_TOKEN_EXPIRE_MINUTES = 7
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        if not token:
            raise credentials_exception

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception