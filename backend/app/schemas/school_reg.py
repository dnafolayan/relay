from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SchoolRegSchema(BaseModel):
    name: str = Field(..., description="Name of the school")
    email: EmailStr = Field(..., description="Email address of the school")
    phone_number: str = Field(..., description="Phone number of the school")

    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    admin_email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(
        ..., description="Password for the user", min_length=8, max_length=128
    )


class SchoolResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str


class AdminResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class SchoolRegResponse(BaseModel):
    message: str
    school: SchoolResponse
    admin: AdminResponse

    model_config = ConfigDict(from_attributes=True)


# todo: study sqlalchemy model configuration
