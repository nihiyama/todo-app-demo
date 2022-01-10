from typing import Optional, List

from fastapi_camelcase import CamelModel
from app.schemas.todo_card import TodoCard


class TodoListBase(CamelModel):
    title: Optional[str]
    detail: Optional[str]


class TodoListCreate(TodoListBase):
    title: str


class TodoListUpdate(TodoListBase):
    card_order: Optional[str] = None


class TodoListInDBBase(TodoListBase):
    id: Optional[int]
    card_order: Optional[str]

    class Config:
        orm_mode = True


class TodoList(TodoListInDBBase):
    todo_cards: List[TodoCard]


class TodoCardInDB(TodoListInDBBase):
    pass
