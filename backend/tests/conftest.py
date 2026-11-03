import subprocess
import sys

import pytest_asyncio
from app.core.config import AppSettings
from app.models.base import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

settings = AppSettings()

DB_TEST_URL = settings.db_test_url.get_secret_value()


def pytest_sessionstart(session):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-x",
            "db=test",
            "upgrade",
            "head",
        ],
        check=True,
    )


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def db_engine():
    test_engine = create_async_engine(DB_TEST_URL, echo=False)
    try:
        yield test_engine
    finally:
        await test_engine.dispose()


@pytest_asyncio.fixture(scope="function", loop_scope="session")
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
