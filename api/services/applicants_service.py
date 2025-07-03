from api.repositories.applicants_repository import ApplicantsRepository
from api.schemas.applicants_schema import ApplicantCreate, ApplicantUpdate, ApplicantResponse, AuthenticatedResponse, JobApplicationCreate, JobApplicationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.utilities.password_manager import PasswordManager
from api.utilities.token_manager import TokenManager

class ApplicantsService:

    def __init__(self):
        self.applicants_repository = ApplicantsRepository()

    # GET APPLICANT FUNCTION
    async def get(self, db_session: AsyncSession, applicant_id: int) -> Optional[ApplicantResponse]:
        applicant = await self.applicants_repository.get(db_session, applicant_id)
        if not applicant:
            return None
        else: 
            return ApplicantResponse.model_validate(applicant)
        
    # CREATE APPLICANT'S ACCOUNT FUNCTION
    async def create(self, db_session: AsyncSession, applicant_data: ApplicantCreate) -> ApplicantResponse:
        is_email_exist = await self.applicants_repository.validate_email(db_session, applicant_data.email_address)

        if is_email_exist:
            return None
        else:
            applicant = await self.applicants_repository.create(db_session, applicant_data)
            if not applicant:
                return None
            else:
                return ApplicantResponse.model_validate(applicant)
            
    # CREATE JOB APPLICATIONS FUNCTION
    async def create_job_application(self, db_session: AsyncSession, applicant_id: int, applications_data: JobApplicationCreate) -> JobApplicationResponse:
        applicant = await self.applicants_repository.get(db_session, applicant_id)
        if not applicant:
            return None
        else:
            job_application = await self.applicants_repository.create_job_application(db_session, applicant_id, applications_data)
            if not job_application:
                return None
            else:
                return JobApplicationResponse.model_validate(job_application)
