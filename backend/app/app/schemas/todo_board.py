from typing import Optional, List

from fastapi_camelcase import CamelModel

from app.schemas.user_todo_board_association import UserTodoBoardAssociation
from app.schemas.todo_list import TodoListBrevity


class TodoBoardBase(CamelModel):
    title: Optional[str] = None
    detail: Optional[str] = None


class TodoBoardCreate(TodoBoardBase):
    title: str


class TodoBoardUpdate(TodoBoardBase):
    useable_user_email_addresses: Optional[List[str]] = None
    useable_user_is_owners: Optional[List[str]] = None
    list_order: Optional[str] = None


class TodoBoardInDBBase(TodoBoardBase):
    uuid: Optional[str] = None
    list_order: Optional[str] = None

    class Config:
        orm_mode = True


class TodoBoard(TodoBoardInDBBase):
    users: List[UserTodoBoardAssociation]
    todo_lists: List[TodoListBrevity]


class TodoBoardBrevity(TodoBoardInDBBase):
    pass


class TodoBoardInDB(TodoBoardInDBBase):
    pass
