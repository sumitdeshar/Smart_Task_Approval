from fastapi import HTTPException, status, Header, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from utils.token import token_utils
from jose import JWTError
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



# def get_current_user(authorization: Optional[str] = Header(None)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )

#     if not authorization or not authorization.startswith("Bearer "):
#         raise credentials_exception

#     token_str = authorization.split(" ")[1]
#     user_id = token_utils.verify_token(token_str, credentials_exception)
#     return user_id

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

# def verify_access_token(request: Request):
#     auth_header = request.headers.get("Authorization")

#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Authorization header missing")

#     token_str = auth_header.split(" ")[1]

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )

#     user_id = token_utils.verify_token(token_str, credentials_exception)
#     return user_id 
