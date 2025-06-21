from api.repositories.users_repository import UsersRepository
from api.schemas.users_schema import UserCreate, UserUpdate, UserResponse, AuthenticatedResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.utilities.password_manager import PasswordManager
from api.utilities.token_manager import TokenManager

class UsersService:

    def __init__(self):
        self.users_repository = UsersRepository()

    # GET USER ID FUNCTION
    async def get(self, db_session: AsyncSession, user_id: int) -> Optional[UserResponse]:
        user = await self.users_repository.get(db_session, user_id)
        if not user:
            return None
        else: 
            return UserResponse.model_validate(user)

    # CREATE USER FUNCTION
    async def create(self, db_session: AsyncSession, user_data: UserCreate) -> UserResponse:
        is_email_exist = await self.users_repository.validate_email(db_session, user_data.email_address)

        if is_email_exist:
            return None
        else:
            user = await self.users_repository.create(db_session, user_data)
            if not user:
                return None
            else:
                return UserResponse.model_validate(user)
    
    # UPDATE USER FUNCTION
    async def update(self, db_session: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        user = await self.users_repository.update(db_session, user_id, user_data)

        if not user:
            return None
        else:
            return UserResponse.model_validate(user)
    
    # DELETE USER FUNCTION
    async def delete(self, db_session: AsyncSession, user_id: int) -> bool:
        user = await self.users_repository.delete(db_session, user_id)

        if not user:
            return None
        else:
            return user
    
    # SOFT DELETE USER FUNCTION
    async def soft_delete(self, db_session: AsyncSession, user_id: int) -> bool:
        user = await self.users_repository.soft_delete(db_session, user_id)

        if not user:
            return None
        else:
            return user
        
    # AUTHENTICATE OR LOGIN FUNCTION
    async def authenticate(self, db_session: AsyncSession, email_address: str, password: str) -> Optional[AuthenticatedResponse]:
        user = await self.users_repository.authenticate(db_session, email_address)

        if not user or not user.accounts:
            return None

        if not PasswordManager.verify_password(password, user.accounts.password):
            return None
        
        access_token = await TokenManager.generate_access_token({
            "id": user.id, 
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email_address": user.email_address,
            "role": user.role
        })
        refresh_token = await TokenManager.generate_refresh_token({
            "id": user.id, 
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email_address": user.email_address,
            "role": user.role
        })

        user_response = UserResponse.model_validate(user)

        return AuthenticatedResponse(
            access_token = access_token,
            refresh_token = refresh_token,
            user = user_response
        )


        