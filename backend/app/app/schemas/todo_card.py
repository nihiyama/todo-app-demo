from typing import Optional, List
from datetime import date

from fastapi_camelcase import CamelModel
from app.schemas.user import UserAssociation


class TodoCardBase(CamelModel):
    title: Optional[str]
    detail: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class TodoCardCreate(TodoCardBase):
    title: str
    assignees_email_address: List[str] = []


class TodoCardUpdate(TodoCardBase):
    assignees_email_address: Optional[List[str]] = None


class TodoCardInDBBase(TodoCardBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class TodoCard(TodoCardInDBBase):
    assignees: List[UserAssociation]


class TodoCardInDB(TodoCardInDBBase):
    pass
