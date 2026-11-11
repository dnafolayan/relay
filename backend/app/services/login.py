from app.core.hasher import verify_password
from app.core.security.jwt import create_access_token
from app.custom_exceptions.auth_service_unavailable_exception import (
    AuthServiceUnavailableException,
)
from app.custom_exceptions.invalid_login_exception import InvalidLoginException
from app.models.user import User
from app.schemas.login import LoginRequest, LoginResponse
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


def _normalize_email(email: str) -> str:
    """
    Normalize the email address by converting it to lowercase and stripping whitespace.
    """
    return email.strip().lower()


async def login(login_data: LoginRequest, session: AsyncSession) -> LoginResponse:
    normalized_email: str = _normalize_email(login_data.email)
    try:
        async with session.begin():
            stmt = select(User).where(func.lower(User.email) == normalized_email)
            user: User | None = (await session.execute(stmt)).scalar_one_or_none()
    except SQLAlchemyError as exc:
        raise AuthServiceUnavailableException(
            message="Authentication service is currently unavailable"
        ) from exc

    if not user:
        raise InvalidLoginException(message="Invalid email or password")

    is_password_valid: bool = await verify_password(
        login_data.password, user.password_hash
    )

    if not is_password_valid:
        raise InvalidLoginException(message="Invalid email or password")

    access_token: str = create_access_token(
        admin_user_id=user.id, admin_school_id=user.school_id
    )

    return LoginResponse(access_token=access_token, token_type="bearer")
