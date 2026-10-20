import asyncio

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

ph = PasswordHasher()


async def hash_password(password: str) -> str:
    """
    Hashes a password using Argon2 algorithm.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    hashed_password = await asyncio.to_thread(ph.hash, password)
    return hashed_password


async def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        hashed_password (str): The hashed password to verify against.
        plain_password (str): The plain text password to verify.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        await asyncio.to_thread(ph.verify, hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except InvalidHashError:
        return False


async def needs_rehash(hashed_password: str) -> bool:
    return await asyncio.to_thread(ph.check_needs_rehash, hashed_password)
