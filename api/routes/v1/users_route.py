from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.controllers.users_controller import UsersController
from api.schemas.users_schema import UserCreate, UserUpdate, UserAuthenticate
from api.utilities.database_connection import get_database

router = APIRouter()

users_controller = UsersController()

@router.get("/{user_id}")
async def get(
   user_id: int,
   db_session: AsyncSession = Depends(get_database)
):
   """
   GET USER DETAILS API
   """
   return await users_controller.get(db_session, user_id)

@router.post("/")
async def create(
   user_data: UserCreate,
   db_session: AsyncSession = Depends(get_database)
):
   """
   CREATE NEW USER ACCOUNT API
   """ 
   return await users_controller.create(db_session, user_data)

@router.patch("/{user_id}")
async def update(
   user_id: int,
   user_data: UserUpdate,
   db_session: AsyncSession = Depends(get_database)
):
   """
   UPDATE USER DETAILS API
   - Only updates fields provided in the request.
   """
   return await users_controller.update(db_session, user_id, user_data)

@router.delete("/{user_id}")
async def delete(
   user_id: int,
   db_session: AsyncSession = Depends(get_database)
):
   """
   DELETE USER DETAILS API
   - Deletes user and their associated account.
   """
   return await users_controller.delete(db_session, user_id)

@router.delete("/soft-delete/{user_id}")
async def soft_delete(
    user_id: int,
    db_session: AsyncSession = Depends(get_database)
):
    """
    SOFT DELETE USER API
    - Soft delete user and their associated account by setting deleted_at timestamp
    """
    return await users_controller.soft_delete(db_session, user_id)

@router.post("/authenticate")
async def authenticate(
   user_data: UserAuthenticate,
   db_session: AsyncSession = Depends(get_database)
):
   """
   AUTHENTICATE OR LOGIN USER ACCOUNT API
   """
   return await users_controller.authenticate(db_session, user_data.email_address, user_data.password)
   