from contextlib import asynccontextmanager

from app.core.config import AppSettings
from app.core.database import engine
from app.core.dependencies.session_generator import get_session
from app.models.base import Base
from app.schemas.user import UserCreate, UserResponse
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

settings = AppSettings()  # app settings
APP_NAME = settings.app_name
API_DESCRIPTION = settings.app_description


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    engine.dispose()


app = FastAPI(title=APP_NAME, description=API_DESCRIPTION, lifespan=lifespan)


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(user: UserCreate):
    try:
        pass
    except Exception as e:
        pass


@app.get("/health")
def health_check():
    return {"status": "ok"}
