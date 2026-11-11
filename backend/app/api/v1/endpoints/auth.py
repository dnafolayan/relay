from app.core.dependencies.session_generator import get_session
from app.schemas.login import LoginRequest, LoginResponse
from app.schemas.school_reg import SchoolRegResponse, SchoolRegSchema
from app.services.login import login
from app.services.register_school import register_school
from fastapi import APIRouter, Depends, HTTPException, status
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
    login_data: LoginRequest, session: AsyncSession = Depends(get_session)
):
    return await login(login_data, session)
