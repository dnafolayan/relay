from app.core.dependencies.session_generator import get_session
from app.schemas.school_reg import SchoolRegResponse, SchoolRegSchema
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
