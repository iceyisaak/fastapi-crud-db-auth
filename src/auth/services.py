from . import models,schemas,utils
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

class User:

    @staticmethod
    async def get_user_by_email(email:str, session:AsyncSession):
        statement=select(models.User).where(models.User.email==email)
        result=await session.exec(statement)
        user=result.first()
        return user
    
    @staticmethod
    async def user_exists(email,session:AsyncSession):
        user=await User.get_user_by_email(email,session)
        return user is not None

    @staticmethod
    async def create_user(user:schemas.UserCreate,session:AsyncSession):
        new_user=user.model_dump()

        created_user=models.User(**new_user)
        created_user.password_hash=utils.hash_password(new_user['password'])
        session.add(created_user)
        await session.commit()
        return created_user

        
    