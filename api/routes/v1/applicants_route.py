from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.controllers.applicants_controller import ApplicantsController
from api.schemas.applicants_schema import ApplicantCreate, ApplicantUpdate, JobApplicationCreate
from api.utilities.database_connection import get_database

router = APIRouter()

applicants_controller = ApplicantsController()

@router.get("/{applicant_id}")
async def get(
   applicant_id: int,
   db_session: AsyncSession = Depends(get_database)
):
   """
   GET APPLICANT DETAILS ENDPOINT
   """
   return await applicants_controller.get(db_session, applicant_id)

@router.post("/")
async def create(
   applicant_data: ApplicantCreate,
   db_session: AsyncSession = Depends(get_database)
):
   """
   CREATE NEW APPLICANT ACCOUNT ENDPOINT
   """ 
   return await applicants_controller.create(db_session, applicant_data)

@router.post("/create-job-application/{applicant_id}")
async def create_job_application(
   applicant_id: int,
   applications_data: JobApplicationCreate,
   db_session: AsyncSession = Depends(get_database)
):
   """
   CREATE JOB APPLICATION ENDPOINT
   """
   return await applicants_controller.create_job_application(db_session, applicant_id, applications_data)