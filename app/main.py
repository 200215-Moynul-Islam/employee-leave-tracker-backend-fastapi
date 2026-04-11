from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

app = FastAPI()

register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/health")
def health():
    return {"message": "Hello World!"}
