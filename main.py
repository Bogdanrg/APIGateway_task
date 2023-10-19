from fastapi import FastAPI

from config import app_settings
from routers.auth_routes import auth_router

app = FastAPI(title=app_settings.APP_TITLE)

app.include_router(auth_router)
