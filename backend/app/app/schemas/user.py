from typing import Optional

from fastapi_camelcase import CamelModel


class UserBase(CamelModel):
    email_address: Optional[str] = None
    user_name: Optional[str] = None


class UserCreate(UserBase):
    email_address: str
    user_name: str
    password: str


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
