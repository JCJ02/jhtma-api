from pydantic import BaseModel, EmailStr, Field, field_validator, FieldValidationInfo
from pydantic_core import PydanticCustomError
from typing import Optional, Annotated
from datetime import datetime
import re

class ApplicantCreate(BaseModel):
    firstname: Annotated[str, Field(min_length=1, description="Firstname is required")]
    lastname: Annotated[str, Field(min_length=1, description="Lastname is required!")]
    email_address: EmailStr
    password: Annotated[str, Field(min_length=8, description="Password must be at least 8 characters long")]
    confirm_password: Annotated[str, Field(min_length=8, description="Confirm Password must be at least 8 characters long")]

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, password: str) -> str:
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")
        return password

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password: str, info: FieldValidationInfo) -> str:
        password = info.data.get("password")
        if password and confirm_password != password:
            raise ValueError("Confirm Password and Password do not match.")
        return confirm_password

class ApplicantUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email_address: Optional[EmailStr] = None
    role: Optional[str] = None


class JobApplicationCreate(BaseModel):
    company_name: str
    job_position: str
    job_type: str
    job_setup: str
    location: str
    application_status: str

class JobApplicationResponse(BaseModel):
    id: int
    company_name: str
    job_position: str
    job_type: str
    job_setup: str
    location: str
    date_applied: datetime
    application_status: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    applicant_id: int

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id: int
    password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    applicant_id: int

    class Config:
        from_attributes = True

class ApplicantResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email_address: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        exclude_unset = True
        exclude_none = True 

class ApplicantAuthenticate(BaseModel):
    email_address: EmailStr
    password: str

class AuthenticatedResponse(BaseModel):
    access_token: str
    refresh_token: str
    applicant: ApplicantResponse

    class Config:
        from_attributes = True