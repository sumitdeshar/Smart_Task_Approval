from fastapi import FastAPI
from config.db import engine
import models

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from Smart Track"}


