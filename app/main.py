from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import health_router, db_health_router

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(db_health_router)
