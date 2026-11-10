import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="First name of the user"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="Last name of the user"
    )
    email: EmailStr = Field(
        ..., max_length=254, description="Email address of the user"
    )
    password: str = Field(
        ..., min_length=8, max_length=128, description="Password of the user"
    )


class UserResponse(BaseModel):
    id: int = Field(..., description="ID of the user")
    role: str = Field(
        ...,
        description="Role of the user",
        examples=["user"],
    )
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="First name of the user"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="Last name of the user"
    )
    email: EmailStr = Field(
        ..., max_length=254, description="Email address of the user"
    )
    created_at: datetime.datetime = Field(
        ..., description="Timestamp of when the user was created"
    )

    model_config = ConfigDict(from_attributes=True)
