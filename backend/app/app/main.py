
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.config import settings

app = FastAPI()

app.mount(settings.MEDIA_URLPATH, StaticFiles(settings.MEDIA_FILEPATH), name="media")
