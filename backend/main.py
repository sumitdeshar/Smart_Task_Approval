from tkinter.filedialog import test

from fastapi import FastAPI
from config.db import engine, get_session, create_tables
from routes.test import test

app = FastAPI()
app.include_router(test, prefix="/test")

#starup actions
@app.on_event("startup")
async def on_startup():
    await create_tables()

@app.get("/")
def read_root():
    return {"message": "Hello from Smart Track"}


