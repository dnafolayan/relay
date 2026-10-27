from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import AppSettings

settings = AppSettings()

DATABASE_URL = settings.db_url.get_secret_value()

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)
