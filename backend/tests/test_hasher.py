import pytest
from app.core.hasher import hash_password, needs_rehash, verify_password


@pytest.mark.asyncio
async def test_hash_password():
    password = "my_secure_password"
    hashed = await hash_password(password)
    assert await verify_password(hashed, password) is True


@pytest.mark.asyncio
async def test_invalid_password_verification():
    password = "my_secure_password"
    hashed = await hash_password(password)
    assert await verify_password(hashed, "wrong_password") is False


@pytest.mark.asyncio
async def test_malformed_hash_verification():
    malformed_hash = "not_a_valid_hash"
    assert await verify_password(malformed_hash, "any_password") is False


@pytest.mark.asyncio
async def test_needs_rehash():
    password = "my_secure_password"
    hashed = await hash_password(password)
    assert await verify_password(hashed, password) is True
    assert await needs_rehash(hashed) is False
