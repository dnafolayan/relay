import asyncpg
from app.core.hasher import hash_password
from app.custom_exceptions.user_already_exists_exception import (
    UserAlreadyExistsException,
)
from app.custom_exceptions.user_registration_exception import (
    UserRegistrationException,
)
from app.custom_exceptions.user_retrieval_exception import (
    UserRetrievalException,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def register_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> UserResponse:
    stmt = select(User).where(User.email == user_in.email)
    existing_user = (await session.execute(stmt)).scalar_one_or_none()

    if existing_user:
        raise UserAlreadyExistsException(
            email=user_in.email, message="User email is already registered"
        )

    password_hash = await hash_password(user_in.password)

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
    except IntegrityError as e:
        await session.rollback()

        orig_err = e.orig

        if isinstance(orig_err, asyncpg.exceptions.PostgresError):

            sql_state = orig_err.sqlstate
            constraint_name = orig_err.constraint_name

            if sql_state == 23505:
                if constraint_name == "uq_users_email":
                    raise UserAlreadyExistsException(
                        email=user_in.email, message="User email is already registered"
                    ) from e
                else:
                    raise UserRegistrationException(
                        email=user_in.email,
                        message=f"failed to commit user due to unique constraint: {constraint_name}",
                    ) from e
            else:
                raise UserRegistrationException(
                    email=user_in.email,
                    message=f"failed to commit user with integrity error code: {sql_state}",
                ) from e
        else:
            raise UserRegistrationException(
                email=user_in.email, message="Generic integrity error"
            ) from e
    except Exception as e:
        await session.rollback()
        raise UserRegistrationException(
            email=user_in.email, message="db transaction failed"
        ) from e

    try:
        await session.refresh(new_user)
    except Exception as e:
        raise UserRetrievalException(
            email=user_in.email, message="failed to reload created user"
        ) from e

    return UserResponse.model_validate(new_user)
