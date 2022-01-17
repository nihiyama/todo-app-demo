from typing import Optional, List
from datetime import date

from fastapi_camelcase import CamelModel
from app.schemas.user import UserAssociation


class TodoCardBase(CamelModel):
    title: Optional[str] = None
    detail: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    todo_list_id: Optional[int] = None


class TodoCardCreate(TodoCardBase):
    title: str
    todo_list_id: int
    assignees_email_address: Optional[List[str]] = None


class TodoCardUpdate(TodoCardBase):
    assignees_email_address: Optional[List[str]] = None


class TodoCardMove(CamelModel):
    todo_list_id_with_before: int
    todo_list_id_with_after: Optional[int]
    card_order_with_before: str
    card_order_with_after: Optional[str]


class TodoCardInDBBase(TodoCardBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class TodoCard(TodoCardInDBBase):
    assignees: List[UserAssociation]


class TodoCardInDB(TodoCardInDBBase):
    pass
