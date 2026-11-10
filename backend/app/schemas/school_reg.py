from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SchoolRegSchema(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=150, description="Name of the school"
    )
    email: EmailStr = Field(
        ..., max_length=254, description="Email address of the school"
    )
    phone_number: str = Field(
        ..., min_length=7, max_length=32, description="Phone number of the school"
    )
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="First name of the user"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="Last name of the user"
    )
    admin_email: EmailStr = Field(
        ..., max_length=254, description="Email address of the user"
    )
    password: str = Field(
        ..., description="Password for the user", min_length=8, max_length=128
    )


class SchoolResponse(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr = Field(..., max_length=254)
    phone_number: str = Field(..., min_length=7, max_length=32)

    model_config = ConfigDict(from_attributes=True)


class AdminResponse(BaseModel):
    id: int
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(..., max_length=254)

    model_config = ConfigDict(from_attributes=True)


class SchoolRegResponse(BaseModel):
    message: str
    school: SchoolResponse
    admin: AdminResponse

    model_config = ConfigDict(from_attributes=True)


# todo: study sqlalchemy model configuration
