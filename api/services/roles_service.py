from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.roles_schema import RoleCreate, RoleUpdate, RoleResponse
from api.repositories.roles_repository import RolesRepository
from typing import Optional

class RolesService:

    def __init__(self):
        self.roles_repository = RolesRepository()

    # GET ROLE FUNCTION
    async def get(self, db_session: AsyncSession, role_id: int) -> Optional[RoleResponse]:
        role = await self.roles_repository.get(db_session, role_id)

        if not role:
            return None
        else:
            return RoleResponse.model_validate(role)

    # CREATE ROLE FUNCTION
    async def create(self, db_session: AsyncSession, role_data: RoleCreate) -> RoleResponse:
        role = await self.roles_repository.create(db_session, role_data)

        if not role:
            return None
        else:
            return RoleResponse.model_validate(role)
        
    # UPDATE ROLE FUNCTION
    async def update(self, db_session: AsyncSession, role_id: int, role_data: RoleUpdate) -> Optional[RoleResponse]:
        role = await self.roles_repository.update(db_session, role_id, role_data)

        if not role:
            return None
        else:
            return RoleResponse.model_validate(role)
        
    # DELETE ROLE FUNCTION
    async def delete(self, db_session: AsyncSession, role_id: int) -> bool:
        role = await self.roles_repository.delete(db_session, role_id)

        if not role:
            return None
        else:
            return role
        
    # SOFT DELETE ROLE FUNCTION
    async def soft_delete(self, db_session: AsyncSession, role_id: int) -> bool:
        role = await self.roles_repository.soft_delete(db_session, role_id)

        if not role:
            return None
        else:
            return role