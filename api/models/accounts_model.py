from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    password = Column(String, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    applicants = relationship("Applicants", back_populates="accounts")
    users = relationship("Users", back_populates="accounts")