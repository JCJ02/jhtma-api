from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email_address: EmailStr
    role: str
    password: str

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email_address: Optional[EmailStr] = None
    role: Optional[str] = None

class AccountResponse(BaseModel):
    id: int
    password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email_address: str
    role: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        exclude_unset = True
        exclude_none = True 

class UserAuthenticate(BaseModel):
    email_address: EmailStr
    password: str

class AuthenticatedResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse

    class Config:
        from_attributes = True