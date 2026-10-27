import pytest
from app.core.dependencies.session_generator import get_session
from sqlalchemy import text


@pytest.mark.asyncio
async def test_get_session():
    async for session in get_session():
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1
