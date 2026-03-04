from fastapi import FastAPI

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from Smart Track"}


