from sqlalchemy.ext.asyncio import AsyncSession
from api.models.roles_model import Roles
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.roles_schema import RoleCreate, RoleUpdate
from typing import Optional
from sqlalchemy import select, delete, update
from sqlalchemy.sql import func

class RolesRepository:
    # GET ROLE FUNCTION
    async def get(self, db_session: AsyncSession, role_id: int) -> str:
        result = await db_session.execute(
            select(Roles).where(Roles.id == role_id).where(Roles.deleted_at.is_(None))
        )
        role = result.scalars().first()
            
        return role

    # CREATE ROLE FUNCTION
    async def create(self, db_session: AsyncSession, role_data: RoleCreate) -> Roles:
        try:
            new_role = Roles(
                role=role_data.role,
                description=role_data.description
            )
            db_session.add(new_role)
            await db_session.commit()
            await db_session.refresh(new_role)

            return new_role
        
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # UPDATE ROLE FUNCTION
    async def update(self, db_session: AsyncSession, role_id: int, role_data: RoleUpdate) -> Optional[Roles]:
        try:
            result = await db_session.execute(
                select(Roles).where(Roles.id == role_id, Roles.deleted_at.is_(None))
            )
            role = result.scalars().first()

            if not role:
                return None
            
            for field, value in role_data.model_dump(exclude_unset=True).items():
                setattr(role, field, value)

            await db_session.commit()
            await db_session.refresh(role)

            return role
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # DELETE ROLE FUNCTION
    async def delete(self, db_session: AsyncSession, role_id: int) -> bool:
        try:
            result = await db_session.execute(
                select(Roles).where(Roles.id == role_id)
            )
            role = result.scalars().first()

            if not role:
                return False

            await db_session.delete(role)
            await db_session.commit()

            return True
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # SOFT DELETE ROLE FUNCTION
    async def soft_delete(self, db_session: AsyncSession, role_id: int) -> bool:
        try:
            result = await db_session.execute(
                select(Roles).where(Roles.id == role_id).where(Roles.deleted_at.is_(None))
            )
            role = result.scalars().first()

            if not role:
                return False
            
            role.deleted_at = func.now()

            await db_session.commit()
            return True
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        