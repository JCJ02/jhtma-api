from api.services.roles_service import RolesService
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.roles_schema import RoleCreate, RoleUpdate, RoleResponse
from api.utilities.app_response import AppResponse

class RolesController:

    def __init__(self):
        self.roles_service = RolesService()

    # GET ROLE FUNCTION
    async def get(self, db_session: AsyncSession, role_id: int) -> str:
        try:
            role = await self.roles_service.get(db_session, role_id)
            
            if not role:
                return AppResponse.send_error(
                    data = None,
                    message = "Role not Found!",
                    code = 404
                )
            else:
                return AppResponse.send_successful(
                    data = role.model_dump(),
                    message = "Role Found!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )

    # CREATE ROLE FUNCTION
    async def create(self, db_session: AsyncSession, role_data: RoleCreate) -> str:
        try:
            create = await self.roles_service.create(db_session, role_data)

            if not create:
                return AppResponse.send_error(
                    data = None,
                    message ="Failed to Create!",
                    code = 403
                )
            else:
                roles_response = RoleResponse.model_validate(create)
                return AppResponse.send_successful(
                    data = roles_response.model_dump(),
                    message = "Successfully Created!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
        
    # UPDATE ROLE FUNCTION
    async def update(self, db_session: AsyncSession, role_id: int, role_data: RoleUpdate) -> str:
        try:
            update = await self.roles_service.update(db_session, role_id, role_data)

            if not update:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Updated!",
                    code = 403
                )
            
            return AppResponse.send_successful(
                data = update.model_dump(),
                message = "Successfully Updated!"
            )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
        
    # DELETE ROLE FUNCTION
    async def delete(self, db_session: AsyncSession, role_id: int) -> str:
        try:
            isDeleted = await self.roles_service.delete(db_session, role_id)
            
            if not isDeleted:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Delete!",
                    code = 403
                )
            else: 
                return AppResponse.send_successful(
                    data = {
                        "message": "Role Deleted!"
                    },
                    message = "Sucessfully Deleted!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
        
    # SOFT DELETE ROLE FUNCTION
    async def soft_delete(self, db_session: AsyncSession, role_id: int) -> str:
        try:
            isSoftDeleted = await self.roles_service.soft_delete(db_session, role_id)

            if not isSoftDeleted:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Soft Delete!",
                    code = 403
                )
            else:
                return AppResponse.send_successful(
                    data = {
                        "message": "Role Soft Deleted!"
                    },
                    message = "Successfully Soft Deleted!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )