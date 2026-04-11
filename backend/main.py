from fastapi import FastAPI
from configs.db import create_tables
from routes.user import user_router as user
from routes.authentication import auth
import os

app = FastAPI()

app.include_router(user)
app.include_router(auth)

#starup actions
@app.on_event("startup")
async def on_startup():
    await create_tables()

@app.get("/")
def read_root():
    SECRET_KEY = os.getenv("SECRET_KEY")
    print('secrect key:', SECRET_KEY)
    return {"message": "Hello from Smart Track"}


