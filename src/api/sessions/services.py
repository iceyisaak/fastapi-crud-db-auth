from . import models
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime


class Session:
    
    @staticmethod
    async def create_session(
        user_uid: str,
        access_token: str,
        refresh_token: str,
        access_jti: str,
        refresh_jti: str,
        expires_at: datetime,
        created_at: datetime,
        session: AsyncSession
    ):
        """Create a new session when user logs in"""
        new_session = models.Session(
            user_uid=uuid.UUID(user_uid),
            access_token=access_token,
            refresh_token=refresh_token,
            access_jti=access_jti,
            refresh_jti=refresh_jti,
            expires_at=expires_at,
            created_at=created_at,
            is_active=True
        )
        session.add(new_session)
        await session.commit()
        await session.refresh(new_session)
        return new_session

    @staticmethod
    async def is_session_active(jti: str, session: AsyncSession) -> bool:
        """Check if a session is active using either access_jti or refresh_jti"""
        statement = select(models.Session).where(
            ((models.Session.access_jti == jti) | (models.Session.refresh_jti == jti)) &
            (models.Session.is_active == True)
        )
        result = await session.exec(statement)
        active_session = result.first()
        return active_session is not None

    @staticmethod
    async def revoke_session(jti: str, session: AsyncSession):
        """Revoke a session using either access_jti or refresh_jti"""
        statement = select(models.Session).where(
            (models.Session.access_jti == jti) | (models.Session.refresh_jti == jti)
        )
        result = await session.exec(statement)
        user_session = result.first()
        
        if user_session:
            user_session.is_active = False
            session.add(user_session)
            await session.commit()
            return user_session
        return None

    @staticmethod
    async def revoke_all_user_sessions(user_uid: str, session: AsyncSession):
        """Revoke all sessions for a specific user"""
        statement = select(models.Session).where(
            (models.Session.user_uid == uuid.UUID(user_uid)) &
            (models.Session.is_active == True)
        )
        result = await session.exec(statement)
        user_sessions = result.all()
        
        for user_session in user_sessions:
            user_session.is_active = False
            session.add(user_session)
        
        await session.commit()
        return len(user_sessions)

    @staticmethod
    async def cleanup_expired_sessions(session: AsyncSession):
        """Remove expired sessions from the database (cleanup task)"""
        statement = select(models.Session).where(
            models.Session.expires_at < datetime.now()
        )
        result = await session.exec(statement)
        expired_sessions = result.all()
        
        for expired_session in expired_sessions:
            await session.delete(expired_session)
        
        await session.commit()
        return len(expired_sessions)

    @staticmethod
    async def get_user_sessions(user_uid: str, session: AsyncSession):
        """Get all active sessions for a user"""
        statement = select(models.Session).where(
            (models.Session.user_uid == uuid.UUID(user_uid)) &
            (models.Session.is_active == True)
        )
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_session_by_jti(jti: str, session: AsyncSession):
        """Get session by access_jti or refresh_jti"""
        statement = select(models.Session).where(
            (models.Session.access_jti == jti) | (models.Session.refresh_jti == jti)
        )
        result = await session.exec(statement)
        return result.first()
