from api.services.applicants_service import ApplicantsService
from api.utilities.app_response import AppResponse
from api.schemas.applicants_schema import ApplicantCreate, ApplicantUpdate, ApplicantResponse, JobApplicationCreate, JobApplicationResponse
from sqlalchemy.ext.asyncio import AsyncSession

class ApplicantsController:

    def __init__(self):
        self.applicants_service = ApplicantsService()

    # GET APPLICANT FUNCTION
    async def get(self, db_session: AsyncSession, applicant_id: int) -> str:
        try:
            applicant = await self.applicants_service.get(db_session, applicant_id)
            if not applicant:
                return AppResponse.send_error(
                    data = None,
                    message = "Applicant not Found!",
                    code = 404
                )
            return AppResponse.send_successful(
                data = applicant.model_dump(),
                message = "Applicant Found!",
                code = 200
            )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )

    # CREATE APPLICANT'S ACCOUNT FUNCTION
    async def create(self, db_session: AsyncSession, applicant_data: ApplicantCreate) -> str:
        try:
            create = await self.applicants_service.create(db_session, applicant_data)
            if not create:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Create!",
                    code = 404
                )
            else:
                applicant_response = ApplicantResponse.model_validate(create)
                return AppResponse.send_successful(
                    data = applicant_response.model_dump(),
                    message = "Successfully Created!",
                    code=201
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
    
    # CREATE JOB APPLICATIONS FUNCTION
    async def create_job_application(self, db_session: AsyncSession, applicant_id: int, applications_data: JobApplicationCreate) -> str:
        try:
            job_application = await self.applicants_service.create_job_application(db_session, applicant_id, applications_data)
            if not job_application:
                return AppResponse.send_error(
                    data=None,
                    message="Failed to Create Job Application!",
                    code=404
                )
            else:
                job_application_response = JobApplicationResponse.model_validate(job_application)
                return AppResponse.send_successful(
                    data=job_application_response.model_dump(),
                    message="Successfully Created Job Application!",
                    code=201
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
