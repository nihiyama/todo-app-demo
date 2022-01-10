from typing import Optional, List

from sqlalchemy.sql.sqltypes import Boolean

from fastapi_camelcase import CamelModel

from app.schemas.user import UserAssociation


class UserTodoBoardAssociation(CamelModel):
    user: UserAssociation
    is_owner: Boolean

    class Config:
        orm_mode = True
