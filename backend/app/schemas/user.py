import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")


class UserResponse(BaseModel):
    id: int = Field(..., description="ID of the user")
    role: str = Field(..., description="Role of the user", examples=["user"])
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    created_at: datetime.datetime = Field(
        ..., description="Timestamp of when the user was created"
    )

    model_config = ConfigDict(from_attributes=True)
