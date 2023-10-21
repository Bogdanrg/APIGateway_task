from fastapi import FastAPI

from config import app_settings
from routers.analytical_service_routes import analytical_service_router
from routers.auth_routes import auth_router
from routers.search_service_routes import search_service_router

app = FastAPI(title=app_settings.APP_TITLE)

app.include_router(auth_router)
app.include_router(search_service_router)
app.include_router(analytical_service_router)
