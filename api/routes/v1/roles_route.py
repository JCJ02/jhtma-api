from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.controllers.roles_controller import RolesController
from api.schemas.roles_schema import RoleCreate
from api.utilities.database_connection import get_database

router = APIRouter()

roles_controller = RolesController()

@router.get("/")
async def get(
    role_id: int,
    db_session: AsyncSession = Depends(get_database)
):
    """
    GET ROLE DETAILS API
    """
    return await roles_controller.get(db_session, role_id)

@router.post("/")
async def create(
    role_data: RoleCreate,
    db_session: AsyncSession = Depends(get_database)
):
    """
    CREATE NEW ROLE API
    """
    return await roles_controller.create(db_session, role_data)

@router.patch("/{role_id}")
async def update(
    role_id: int,
    role_data: RoleCreate,
    db_session: AsyncSession = Depends(get_database)
):
    """
    UPDATE ROLE DETAILS API
    - Only updates fields provided in the request.
    """
    return await roles_controller.update(db_session, role_id, role_data)

@router.delete("/{role_id}")
async def delete(
    role_id: int,
    db_session: AsyncSession = Depends(get_database)
):
    """
    DELETE ROLE DETAILS API
    """
    return await roles_controller.delete(db_session, role_id)

@router.delete("/soft-delete/{role_id}")
async def soft_delete(
    role_id: int,
    db_session: AsyncSession = Depends(get_database)
):
    """
    SOFT DELETE ROLE DETAILS API
    """
    return await roles_controller.soft_delete(db_session, role_id)