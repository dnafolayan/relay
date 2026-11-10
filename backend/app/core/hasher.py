import asyncio

from app.custom_exceptions.password_processing_exception import (
    PasswordProcessingException,
)
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

ph = PasswordHash.recommended()


async def hash_password(password: str) -> str:
    """
    Hashes a password using the configured pwdlib hasher.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    try:
        return await asyncio.to_thread(ph.hash, password)
    except (TypeError, ValueError) as e:
        raise PasswordProcessingException("Invalid password value") from e


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        return bool(await asyncio.to_thread(ph.verify, plain_password, hashed_password))
    except (TypeError, ValueError) as e:
        raise PasswordProcessingException("Invalid password value or hash") from e
    except UnknownHashError as e:
        raise PasswordProcessingException("Invalid password value or hash") from e


async def verify_and_update(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    try:
        return await asyncio.to_thread(
            ph.verify_and_update, plain_password, hashed_password
        )
    except (TypeError, ValueError) as e:
        raise PasswordProcessingException("Invalid password value or hash") from e
    except UnknownHashError as e:
        raise PasswordProcessingException("Invalid password value or hash") from e
    # only check if a hash needs rehashing after a user has logged in successfully
