from typing import Optional, List

from fastapi_camelcase import CamelModel

from app.schemas.user_todo_board_association import UserTodoBoardAssociation
from app.schemas.todo_list import TodoList


class TodoBoardBase(CamelModel):
    title: Optional[str] = None
    detail: Optional[str] = None


class TodoBoardCreate(TodoBoardBase):
    title: str


class TodoBoardUpdate(TodoBoardBase):
    useable_user_email_address: List[str]
    useable_user_is_owner: List[str]
    list_order: Optional[str]


class TodoBoardInDBBase(TodoBoardBase):
    uuid: Optional[str] = None
    list_order: Optional[str] = None

    class Config:
        orm_mode = True


class TodoBoard(TodoBoardInDBBase):
    useable_user: List[UserTodoBoardAssociation]
    todo_lists: List[TodoList]


class TodoBoardInDB(TodoBoardInDBBase):
    pass
