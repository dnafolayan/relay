import pytest
from app.core.hasher import verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_register import register_user
from sqlalchemy import select


@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(db_session):
    valid_user_in = UserCreate(
        first_name="Sarah",
        last_name="Doe",
        email="sarahdoe@example.com",
        password="sarahdoe1234",
    )

    created_user: UserResponse = await register_user(valid_user_in, db_session)

    assert isinstance(created_user, UserResponse)
    assert created_user.first_name == valid_user_in.first_name
    assert created_user.last_name == valid_user_in.last_name
    assert created_user.email == valid_user_in.email

    stmt = select(User).where(User.email == valid_user_in.email)
    existing_user = (await db_session.execute(stmt)).scalar_one_or_none()

    assert existing_user is not None

    assert existing_user.first_name == valid_user_in.first_name
    assert existing_user.last_name == valid_user_in.last_name
    assert existing_user.email == valid_user_in.email
    assert existing_user.password_hash != valid_user_in.password

    is_password_verified = await verify_password(
        existing_user.password_hash, valid_user_in.password
    )
    assert is_password_verified is True
