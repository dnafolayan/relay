from app.core.hasher import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.custom_exceptions.password_processing_exception import (
    PasswordProcessingException,
)
from backend.app.custom_exceptions.user_already_exists_exception import (
    UserAlreadyExistsException,
)
from backend.app.custom_exceptions.user_registration_exception import (
    UserRegistrationException,
)


async def register_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> UserResponse:
    stmt = select(User).where(User.email == user_in.email)
    existing_user = (await session.execute(stmt)).scalar_one_or_none()

    if existing_user:
        raise UserAlreadyExistsException(email=user_in.email)

    try:
        password_hash = await hash_password(user_in.password)
    except Exception as e:
        raise PasswordProcessingException(detail=str(e))

    new_user = User(
        role="user",
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password_hash=password_hash,
    )

    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)
    except Exception as e:
        await session.rollback()
        raise UserRegistrationException(email=user_in.email, message=str(e))

    return UserResponse(
        id=new_user.id,
        role=new_user.role,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        created_at=new_user.created_at,
    )
