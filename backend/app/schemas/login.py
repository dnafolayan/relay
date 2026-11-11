from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: Literal["bearer"] = Field(
        ..., default="bearer", description="Type of the token, usually 'bearer'"
    )
