from fastapi import APIRouter

from app.api.api_v1 import (
    auth, signup, users
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(signup.router, prefix="/signup", tags=["signup"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
