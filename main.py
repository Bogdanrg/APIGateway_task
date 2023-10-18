from fastapi import FastAPI

from config import app_settings

app = FastAPI(title=app_settings.APP_TITLE)
