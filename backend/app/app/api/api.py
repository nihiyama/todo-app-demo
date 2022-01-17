from fastapi import APIRouter

from app.api.api_v1 import (
    auth, todo_boards, todo_cards, todo_lists, move,
    signup, users
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(todo_boards.router, prefix="/todo-boards", tags=["todo_boards"])
api_router.include_router(todo_cards.router, prefix="/todo-cards", tags=["todo_cards"])
api_router.include_router(todo_lists.router, prefix="/todo-lists", tags=["todo_lists"])
api_router.include_router(move.router, prefix="/move", tags=["move"])
api_router.include_router(signup.router, prefix="/signup", tags=["signup"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
