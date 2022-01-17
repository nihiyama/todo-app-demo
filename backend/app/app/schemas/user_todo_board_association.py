from fastapi_camelcase import CamelModel

from app.schemas.user import UserAssociation


class UserTodoBoardAssociation(CamelModel):
    user: UserAssociation
    is_owner: bool = False

    class Config:
        orm_mode = True
