from app.core.config import AppSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

settings = AppSettings()

DATABASE_URL = settings.db_url.get_secret_value()

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)
