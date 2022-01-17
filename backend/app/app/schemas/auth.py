from fastapi_camelcase import CamelModel


class AuthBase(CamelModel):
    pass


class UserAuth(AuthBase):
    email_address: str
    password: str
