from api.services.users_service import UsersService
from api.utilities.app_response import AppResponse
from api.schemas.users_schema import UserCreate, UserUpdate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

class UsersController:

    def __init__(self):
        self.users_service = UsersService()

    # GET USER FUNCTION
    async def get(self, db_session: AsyncSession, user_id: int) -> str:
        try:
            user = await self.users_service.get(db_session, user_id)
            if not user:
                return AppResponse.send_error(
                    data = None,
                    message = "User not Found!",
                    code = 404
                )
            return AppResponse.send_successful(
                data = user.model_dump(),
                message = "User Found!"
            )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )

    # CREATE USER FUNCTION
    async def create(self, db_session: AsyncSession, user_data: UserCreate) -> str:
        try:
            create = await self.users_service.create(db_session, user_data)
            if not create:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Create!",
                    code = 404
                )
            else:
                user_response = UserResponse.model_validate(create)
                return AppResponse.send_successful(
                    data = user_response.model_dump(),
                    message = "Successfully Created!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
        
    # UPDATE USER FUNCTION
    async def update(self, db_session: AsyncSession, user_id: int, user_data: UserUpdate) -> str:
        try:
            update = await self.users_service.update(db_session, user_id, user_data)

            if not update:
                return AppResponse.send_error(
                    data = None,
                    message = "Failed to Update!",
                    code = 404
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
        
    # DELETE USER FUNCTION
    async def delete(self, db_session: AsyncSession, user_id: int) -> str:
        try:
            isDeleted = await self.users_service.delete(db_session, user_id)
            if not isDeleted:
                return AppResponse.send_error(
                    data=None,
                    message="Failed to Delete!",
                    code=404
                )
            else:
                return AppResponse.send_successful(
                    data={
                        "message": "User Deleted!"
                    },
                    message="Successfully Deleted!"
                )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )
        
    # SOFT DELETE USER FUNCTION
    async def soft_delete(self, db_session: AsyncSession, user_id: int) -> str:
        try:
            isSoftDeleted = await self.users_service.soft_delete(db_session, user_id)
            if not isSoftDeleted:
                return AppResponse.send_error(
                    data=None,
                    message="Failed to Delete!",
                    code=404
                )
            return AppResponse.send_successful(
                data={
                    "message": "User Deleted!"
                },
                message="Successfully Deleted!"
            )
        except Exception as error:
            return AppResponse.send_error(
                data=None,
                message=str(error),
                code=500
            )
    
    # AUTHENTICATION OR LOGIN FUNCTION
    async def authenticate(self, db_session: AsyncSession, email_address: str, password: str) -> str:
        try:
            authenticated = await self.users_service.authenticate(db_session, email_address, password)

            if not authenticated:
                return AppResponse.send_error(
                    data = None,
                    message = "Invalid Credentials!",
                    code = 401
                )
            return AppResponse.send_successful(
                data = authenticated.model_dump(),
                message = "Logged in Successfully!",
                code = 200
            )
        except Exception as error:
            return AppResponse.send_error(
                data = None,
                message = str(error),
                code = 500
            )