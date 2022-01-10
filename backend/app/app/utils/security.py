from datetime import timedelta
import secrets

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from passlib.context import CryptContext

from app.utils.config import settings

ALGOLITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CookieJwtSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = ALGOLITHM
    authjwt_token_location: set = {"cookies"}
    authjwt_access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    authjwt_access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES*24)
    authjwt_cookie_samesite: str = "strict"
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_cookie_path: str = settings.URL_PREFIX
    authjwt_refresh_cookie_path: str = settings.URL_PREFIX


class CookieAuthJwt(AuthJWT):
    pass

@CookieAuthJwt.load_config
def get_cookie_config():
    return CookieJwtSettings()


class BearerJwtSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_algorithm: str = ALGOLITHM
    authjwt_access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


class BaererAuthJwt(AuthJWT):
    pass

@BaererAuthJwt.load_config
def get_bearer_config():
    return BearerJwtSettings()

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def get_uuid(length: int = 32) -> str:
    return secrets.token_urlsafe(length)
