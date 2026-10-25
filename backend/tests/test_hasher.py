from unittest.mock import AsyncMock

import pytest
from app.core import hasher
from argon2 import PasswordHasher


@pytest.mark.asyncio
async def test_hash_password():
    password = "my_secure_password"
    hashed = await hasher.hash_password(password)
    assert await hasher.verify_password(hashed, password) is True


@pytest.mark.asyncio
async def test_invalid_password_verification():
    password = "my_secure_password"
    hashed = await hasher.hash_password(password)
    assert await hasher.verify_password(hashed, "wrong_password") is False


@pytest.mark.asyncio
async def test_malformed_hash_verification():
    malformed_hash = "not_a_valid_hash"
    assert await hasher.verify_password(malformed_hash, "any_password") is False


@pytest.mark.asyncio
async def test_needs_rehash():
    ph_legacy = PasswordHasher(memory_cost=16384, time_cost=2, parallelism=2)
    password = "my_secure_password"
    hashed = ph_legacy.hash(password)
    assert await hasher.verify_password(hashed, password) is True
    assert await hasher.needs_rehash(hashed) is True


@pytest.mark.asyncio
async def test_hash_password_delegates_to_thread(monkeypatch):
    mocked_to_thread = AsyncMock(return_value="hashed_password")
    monkeypatch.setattr(hasher.asyncio, "to_thread", mocked_to_thread)

    result = await hasher.hash_password("my_secure_password")
    assert result == "hashed_password"

    mocked_to_thread.assert_awaited_with(hasher.ph.hash, "my_secure_password")


@pytest.mark.asyncio
async def test_verify_password_delegates_to_thread(monkeypatch):
    mocked_to_thread = AsyncMock(return_value=False)
    monkeypatch.setattr(hasher.asyncio, "to_thread", mocked_to_thread)

    result = await hasher.verify_password("hashed_password", "my_secure_password")
    assert result is False

    mocked_to_thread.assert_awaited_with(
        hasher.ph.verify, "hashed_password", "my_secure_password"
    )
