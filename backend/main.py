from fastapi import FastAPI
from configs.db import create_tables
from routes.user import user_router as user
from routes.authentication import auth
from routes.tasks import task_router as task
from configs.logging import  setup_logging
# from middleware.api_logger import APILoggerMiddleware
import os

setup_logging()

app = FastAPI()

app.include_router(user)
app.include_router(auth)
app.include_router(task)

# app.add_middleware(APILoggerMiddleware)

#starup actions
@app.on_event("startup")
async def on_startup():
    await create_tables()

@app.get("/")
def read_root():
    SECRET_KEY = os.getenv("SECRET_KEY")
    # print('secrect key:', SECRET_KEY)
    return {"message": "Hello from Smart Track"}


