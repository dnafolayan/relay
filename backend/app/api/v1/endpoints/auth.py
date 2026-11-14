from app.core.config import settings
from app.core.dependencies.session_generator import get_session
from app.schemas.login import LoginRequest, LoginResponse
from app.schemas.school_reg import SchoolRegResponse, SchoolRegSchema
from app.services.login import login as login_service
from app.services.register_school import register_school
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Authentication"])


@router.post(
    "/register-school",
    response_model=SchoolRegResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_school_endpoint(
    reg_data: SchoolRegSchema, session: AsyncSession = Depends(get_session)
):
    return await register_school(reg_data, session)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login_endpoint(
    login_data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    result = await login_service(login_data, session)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        max_age=settings.refresh_token_expire_days * 86400,
        httponly=True,
        samesite="lax",
        secure=settings.app_description == "production",
        path="/api/v1/auth",
    )

    return LoginResponse(access_token=result.access_token, token_type="bearer")
