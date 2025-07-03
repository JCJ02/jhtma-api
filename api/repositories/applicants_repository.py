from sqlalchemy import select, delete, update
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from api.models.applicants_model import Applicants
from api.models.accounts_model import Accounts
from api.models.applicants_model import JobApplications
from api.schemas.applicants_schema import ApplicantCreate, JobApplicationCreate
from api.utilities.password_manager import PasswordManager

class ApplicantsRepository:
    # GET APPLICANT FUNCTION
    async def get(self, db_session: AsyncSession, applicant_id: int) -> Optional[Applicants]:
        result = await db_session.execute(
            select(Applicants).where(Applicants.id == applicant_id).where(Applicants.deleted_at.is_(None))
        )
        applicant = result.scalars().first()
        
        return applicant
    
    # VALIDATE EMAIL FUNCTION
    async def validate_email(self, db_session: AsyncSession, email_address: str) -> Optional[Applicants]:
        result = await db_session.execute(
            select(Applicants).where(Applicants.email_address == email_address).where(Applicants.deleted_at.is_(None))
        )
        is_email_exist = result.scalars().first()

        return is_email_exist
    
    # CREATE APPLICANT'S ACCOUNT FUNCTION
    async def create(self, db_session: AsyncSession, applicant_data: ApplicantCreate) -> Applicants:
        try:
            new_applicant = Applicants(
                firstname=applicant_data.firstname,
                lastname=applicant_data.lastname,
                email_address=applicant_data.email_address,
            )
        
            db_session.add(new_applicant)
            await db_session.flush()

            # Hash the password using PasswordManager
            hashed_password = PasswordManager.hash_password(applicant_data.password)

            new_account = Accounts(
                applicant_id=new_applicant.id,
                password=hashed_password
            )

            db_session.add(new_account)
            await db_session.commit()
            await db_session.refresh(new_applicant)

            return new_applicant

        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # CREATE JOB APPLICATIONS FUNCTION
    async def create_job_application(self, db_session: AsyncSession, applicant_id: int, applications_data: JobApplicationCreate) -> Applicants:
        try:
            job_application = JobApplications(
                company_name=applications_data.company_name,
                job_position=applications_data.job_position,
                job_type=applications_data.job_type,
                job_setup=applications_data.job_setup,
                location=applications_data.location,
                application_status=applications_data.application_status,
                applicant_id=applicant_id
            )

            db_session.add(job_application)
            await db_session.commit()
            await db_session.refresh(job_application)

            return job_application
        
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")

    