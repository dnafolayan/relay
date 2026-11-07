import asyncpg
from app.core.hasher import hash_password
from app.custom_exceptions.school_admin_already_exists import (
    SchoolAdminAlreadyExistsException,
)
from app.custom_exceptions.school_already_exists_exception import (
    SchoolAlreadyExistsException,
)
from app.models.school import School
from app.models.user import User
from app.schemas.school_reg import (
    AdminResponse,
    SchoolRegResponse,
    SchoolRegSchema,
    SchoolResponse,
)
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


def _normalize_email(value: str) -> str:
    return value.strip().lower()


async def register_school(
    reg_data: SchoolRegSchema, session: AsyncSession
) -> SchoolRegResponse:
    school_email = _normalize_email(str(reg_data.email))
    admin_email = _normalize_email(str(reg_data.admin_email))

    admin_password_hash = await hash_password(reg_data.password)

    try:
        async with session.begin():

            school_stmt = select(School).where(func.lower(School.email) == school_email)
            existing_school = (await session.execute(school_stmt)).scalar_one_or_none()

            if existing_school:
                raise SchoolAlreadyExistsException(
                    email=school_email, message="School email is already registered"
                )

            admin_stmt = select(User).where(func.lower(User.email) == admin_email)
            existing_admin = (await session.execute(admin_stmt)).scalar_one_or_none()

            if existing_admin:
                raise SchoolAdminAlreadyExistsException(email=admin_email)

            new_school = School(
                name=reg_data.name,
                email=school_email,
                phone_number=reg_data.phone_number,
            )
            session.add(new_school)
            await session.flush()

            new_admin = User(
                school_id=new_school.id,
                first_name=reg_data.first_name,
                last_name=reg_data.last_name,
                email=admin_email,
                password_hash=admin_password_hash,
            )
            session.add(new_admin)
            await session.flush()
    except IntegrityError as e:
        orig_err = e.orig

        if isinstance(orig_err, asyncpg.exceptions.PostgresError):
            sql_state = getattr(orig_err, "sqlstate", None)
            constraint_name = getattr(orig_err, "constraint_name", None)

            if sql_state == "23505":
                if constraint_name == "schools_email_key":
                    raise SchoolAlreadyExistsException(
                        email=school_email,
                        message="School email is already registered",
                    ) from e
                if constraint_name == "users_email_key":
                    raise SchoolAdminAlreadyExistsException(email=admin_email) from e
                if constraint_name == "schools_phone_number_key":
                    raise SchoolAlreadyExistsException(
                        email=school_email,
                        message="School phone number is already registered",
                    ) from e
        raise

    school_response: SchoolResponse = SchoolResponse.model_validate(new_school)
    admin_response: AdminResponse = AdminResponse.model_validate(new_admin)

    return SchoolRegResponse(
        message="School and admin registered successfully",
        school=school_response,
        admin=admin_response,
    )
