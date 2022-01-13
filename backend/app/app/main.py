from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.utils.config import settings

url_prefix = Path(f"//{settings.URL_PREFIX}")
api_prefix = url_prefix / settings.API_V1_STR
openapi_url = api_prefix / "openapi.json"
docs_url = url_prefix / settings.DOCS_URL
media_url = url_prefix / settings.MEDIA_URLPATH
print(docs_url)
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=str(openapi_url),
    docs_url=str(docs_url)
)
app.mount(str(media_url), StaticFiles(directory=settings.MEDIA_FILEPATH), name="media")

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(api_router, prefix=str(api_prefix))
