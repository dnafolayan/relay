import pytest_asyncio
from app.core.config import AppSettings
from app.models.base import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

settings = AppSettings()

TEST_DB_URL = settings.test_db_url.get_secret_value()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    test_engine = create_async_engine(TEST_DB_URL, echo=False)
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield test_engine
    finally:
        try:
            async with test_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        finally:
            await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    TestAsyncSessionLocal = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            stmt = text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
            await session.execute(stmt)
            await session.commit()
