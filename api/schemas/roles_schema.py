from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleCreate(BaseModel):
    role: str
    description: str

class RoleUpdate(BaseModel):
    role: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    role: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True