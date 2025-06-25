from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class Applicants(Base): 
    __tablename__ = 'applicants'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    email_address = Column(String, index=True)
    role = Column(String, server_default="Applicant", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    accounts = relationship("Accounts", back_populates="applicants", uselist=False) 
    job_applications = relationship("JobApplications", back_populates="applicants", uselist=False)

class JobApplications(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    company_name = Column(String, index=True)
    job_position = Column(String, index=True)
    job_type = Column(String, index=True) # Options = Full-time, Part-time, Contract, Internship
    job_setup = Column(String, index=True) # Options = Remote Work, Onsite, Hybrid
    location = Column(String, index=True)
    date_applied = Column(DateTime(timezone=True), server_default=func.now())
    application_status = Column(String, server_default="Submitted - Pending Response", index=True) # Options = Accepted, Rejected, Submitted - Pending Response, Initial Interviewed, Technical Interviewed, Final Interviewed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))

    applicants =relationship("Applicants", back_populates="job_applications")