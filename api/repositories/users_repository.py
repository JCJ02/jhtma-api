from sqlalchemy import select, delete, update
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from api.models.users_model import Users, Accounts
from api.utilities.password_manager import PasswordManager
from api.schemas.users_schema import UserCreate, UserUpdate
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload

class UsersRepository:
    # GET USER ID FUNCTION
    async def get(self, db_session: AsyncSession, user_id: int) ->  Optional[Users]:
        result = await db_session.execute(
            select(Users).where(Users.id == user_id).where(Users.deleted_at.is_(None))
        )
        user = result.scalars().first()
        
        return user
    
    # VALIDATE EMAIL FUNCTION
    async def validate_email(self, db_session: AsyncSession, email_address: str) -> Optional[Users]:
        result = await db_session.execute(
            select(Users).where(Users.email_address == email_address).where(Users.deleted_at.is_(None))
        )
        is_email_exist = result.scalars().first()

        return is_email_exist

    # CREATE USER FUNCTION
    async def create(self, db_session: AsyncSession, user_data: UserCreate) -> Users:
        try:
            new_user = Users(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email_address=user_data.email_address,
                role=user_data.role,
            )

            db_session.add(new_user)
            await db_session.flush()

            # Hash the password using PasswordManager
            hashed_password = PasswordManager.hash_password(user_data.password)

            new_account = Accounts(
                user_id=new_user.id,
                password=hashed_password, 
            )

            db_session.add(new_account)
            await db_session.commit()
            await db_session.refresh(new_user)

            return new_user
        
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # UPDATE USER FUNCTION
    async def update(self, db_session: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[Users]:
        try:
            result = await db_session.execute(
                select(Users).where(Users.id == user_id, Users.deleted_at.is_(None))
            )
            user = result.scalars().first()

            if not user:
                return None
            
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)

            await db_session.commit()
            await db_session.refresh(user)
            
            return user
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
    
    # DELETE USER FUNCTION
    async def delete(self, db_session: AsyncSession, user_id: int) -> bool:
        try:
            result = await db_session.execute(
                select(Users).where(Users.id == user_id)
            )
            user = result.scalars().first()
        
            if not user:
                return False

            await db_session.execute(
                delete(Accounts).where(Accounts.user_id == user_id)
            )

            await db_session.delete(user)
            await db_session.commit()

            return True
        except SQLAlchemyError  as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # SOFT DELETE USER FUNCTION
    async def soft_delete(self, db_session: AsyncSession, user_id: int) -> bool:
        try:
            result = await db_session.execute(
                select(Users).where(Users.id == user_id).where(Users.deleted_at.is_(None))
            )
            user = result.scalars().first()

            if not user:
                return False
            
            user.deleted_at = func.now()

            await db_session.execute(
                update(Accounts)
                .where(Accounts.user_id == user_id)
                .values(deleted_at=func.now())
            )
            
            await db_session.commit()
            return True
        
        except SQLAlchemyError as error:
            await db_session.rollback()
            raise Exception(f"Database Error: {str(error)}")
        
    # AUTHENTICATE OR LOGIN FUNCTION
    async def authenticate(self, db_session: AsyncSession, email_address: str) -> Optional[Users]:
        result = await db_session.execute(
            select(Users)
            .options(selectinload(Users.accounts))
            .where(Users.email_address == email_address)
            .where(Users.deleted_at.is_(None))
        )
        return result.scalars().first()
    