from fastapi import FastAPI
# Testing code
from app.core.config import settings

app = FastAPI()

@app.get("/health")
def health():
    return {"message": "Hello World!"}
