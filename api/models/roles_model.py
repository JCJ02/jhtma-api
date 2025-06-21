from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from . import Base

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    role = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)