import secrets
import os
from typing import (
    List, Union, Optional
)

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    URL_PREFIX: str = os.getenv("URL_PREFIX", "/")

    @validator("URL_PREFIX", pre=True, allow_reuse=True)
    def assemble_url_prefix(cls, v: str) -> str:
        if v == "":
            return "/"
        elif v[0] != "/":
            return "/" + v
        else:
            return v

    API_V1_STR: str = os.getenv("API_V1_STR", "/")

    @validator("API_V1_STR", pre=True, allow_reuse=True)
    def assemble_api_v1_str(cls, v: str) -> str:
        if v == "":
            return "/"
        elif v[0] != "/":
            return "/" + v
        else:
            return v

    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    SERVER_NAME: str = os.getenv("SERVER_NAME", "project")
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", "http://0.0.0.0,http://0.0.0.0:8000").split(",")

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_backend_cors_origins(cls, v: List[str]) -> List[str]:
        return [e.strip() for e in v]
    
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "fastapi")
    DOCS_URL: str = os.getenv("DOCS_URL", "admin-site")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "changeme")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
    )
    DB_SECRET_KEY: str = os.getenv("DB_SECRET_KEY", "changeme")

    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changeme")

    EMAIL_SENDER_NAME: str = os.getenv("EMAIL_SENDER_NAME", "example")
    EMAIL_SENDER_ADDRESS: str = os.getenv("EMAIL_SENDER_ADDRESS", "example@example.com")
    EMAIL_SERVER_HOST: str = os.getenv("EMAIL_SERVER_HOST", "changeme")
    EMAIL_SERVER_PORT: int = int(os.getenv("EMAIL_SERVER_PORT", "587"))
    EMAIL_HOST_USER: str = os.getenv("EMAIL_HOST_USER", "changeme")
    EMAIL_HOST_PASSWORD: str = os.getenv("EMAIL_HOST_USER", "changeme")

    LOG_FILEPATH: str = os.getenv("LOG_FILEPATH", "/opt/logs/app.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    LOG_HANDLER: str = os.getenv("LOG_HANDLER", "stream")

    class Config:
        case_sensitive = True


settings = Settings()
    
    
    
    

