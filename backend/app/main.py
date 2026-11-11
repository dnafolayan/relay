from contextlib import asynccontextmanager

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.database import engine
from app.core.exception_handlers import (
    register_exception_handlers,
)
from app.models.base import Base
from fastapi import FastAPI

APP_NAME = settings.app_name
API_DESCRIPTION = settings.app_description


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(title=APP_NAME, description=API_DESCRIPTION, lifespan=lifespan)

app.include_router(api_router)

register_exception_handlers(app)
