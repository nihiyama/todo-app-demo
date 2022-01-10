from typing import Optional

from sqlalchemy.sql.sqltypes import Boolean

from fastapi_camelcase import CamelModel


class UserBase(CamelModel):
    email_address: Optional[str] = None
    user_name: Optional[str] = None
    is_superuser: Optional[Boolean] = False


class UserCreate(UserBase):
    email_address: str
    user_name: str
    password: str
    is_superuser: Boolean = False


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    uuid: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class UserAssociation(CamelModel):
    email_address: Optional[str] = None
    user_name: Optional[str] = None

    class Config:
        orm_mord = True
