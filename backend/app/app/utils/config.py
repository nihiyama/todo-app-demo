import secrets
from typing import Any, Dict, List, Literal, Union, Optional

from pydantic import BaseSettings, validator, PostgresDsn, AnyHttpUrl


class Settings(BaseSettings):
    URL_PREFIX: str = "/"

    @validator("URL_PREFIX", pre=True, allow_reuse=True)
    def assemble_url_prefix(cls, v: str) -> str:
        if v == "":
            return "/"
        elif v[0] != "/":
            return "/" + v
        else:
            return v

    API_V1_STR: str = "api/v1"

    @validator("API_V1_STR", pre=True, allow_reuse=True)
    def assemble_api_v1_str(cls, v: str) -> str:
        if v[0] == "/":
            return v[1:]
        else:
            return v

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SERVER_NAME: str = "project"
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, Literal["*"]]] = ["http://0.0.0.0", "http://0.0.0.0:8000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_backend_cors_origins(cls, v: List[str]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    PROJECT_NAME: str = "fastapi"
    DOCS_URL: str = "admin-site"

    @validator("DOCS_URL", pre=True, allow_reuse=True)
    def assemble_docs_url(cls, v: str) -> str:
        if v[0] == "/":
            return v[1:]
        else:
            return v

    SERVICE_URL: str = "http://example.com"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "postgres"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    DB_SECRET_KEY: str = "changeme"

    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "changeme"

    EMAIL_SENDER_NAME: str = "example"
    EMAIL_SENDER_ADDRESS: str = "example@example.com"
    EMAIL_SERVER_HOST: str = "changeme"
    EMAIL_SERVER_PORT: int = 587
    EMAIL_HOST_USER: str = "changeme"
    EMAIL_HOST_PASSWORD: str = "changeme"

    MEDIA_FILEPATH: str = "/opt/app/media"
    MEDIA_URLPATH: str = "media"

    @validator("MEDIA_URLPATH", pre=True, allow_reuse=True)
    def assemble_media_urlpath(cls, v: str) -> str:
        if v[0] == "/":
            return v[1:]
        else:
            return v

    LOG_FILEPATH: str = "/opt/logs/app.log"
    LOG_LEVEL: str = "info"
    LOG_HANDLER: str = "stream"

    class Config:
        case_sensitive = True


settings = Settings()
