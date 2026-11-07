from app.custom_exceptions.password_processing_exception import (
    PasswordProcessingException,
)
from app.custom_exceptions.school_admin_already_exists import (
    SchoolAdminAlreadyExistsException,
)
from app.custom_exceptions.school_already_exists_exception import (
    SchoolAlreadyExistsException,
)
from app.custom_exceptions.school_phone_number_already_exists_exception import (
    SchoolPhoneNumberAlreadyExistsException,
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


async def school_already_exists_handler(
    request: Request, exc: SchoolAlreadyExistsException
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def school_phone_number_already_exists_handler(
    request: Request, exc: SchoolPhoneNumberAlreadyExistsException
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def school_admin_already_exists_handler(
    request: Request, exc: SchoolAdminAlreadyExistsException
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def password_processing_exception_handler(
    request: Request, exc: PasswordProcessingException
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        SchoolAlreadyExistsException, school_already_exists_handler
    )
    app.add_exception_handler(
        SchoolPhoneNumberAlreadyExistsException,
        school_phone_number_already_exists_handler,
    )
    app.add_exception_handler(
        SchoolAdminAlreadyExistsException, school_admin_already_exists_handler
    )
    app.add_exception_handler(
        PasswordProcessingException, password_processing_exception_handler
    )
