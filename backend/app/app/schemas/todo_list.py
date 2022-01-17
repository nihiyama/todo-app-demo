from typing import Optional, List

from fastapi_camelcase import CamelModel
from app.schemas.todo_card import TodoCard


class TodoListBase(CamelModel):
    title: Optional[str] = None
    detail: Optional[str] = None


class TodoListCreate(TodoListBase):
    title: str
    todo_board_uuid: str


class TodoListUpdate(TodoListBase):
    card_order: Optional[str] = None


class TodoListMove(CamelModel):
    todo_board_uuid: str
    new_list_order: str


class TodoListInDBBase(TodoListBase):
    id: Optional[int] = None
    card_order: Optional[str] = None

    class Config:
        orm_mode = True


class TodoList(TodoListInDBBase):
    todo_cards: List[TodoCard]


class TodoListBrevity(TodoListInDBBase):
    pass


class TodoCardInDB(TodoListInDBBase):
    pass
