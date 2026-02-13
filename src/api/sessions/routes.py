"""
Session management endpoints
"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from . import services, schemas
from ..auth import dependencies
from ...db import main
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.get("/sessions", response_model=schemas.SessionListResponse)
async def get_active_sessions(
    current_user = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(main.get_session_context)
):
    """
    Get all active sessions for the current user
    Shows when each session was created and when it expires
    """
    session_service = services.Session()
    user_sessions = await session_service.get_user_sessions(
        user_uid=str(current_user.uid),
        session=session
    )
    
    return schemas.SessionListResponse(
        sessions=[
            schemas.SessionResponse.model_validate(s)
            for s in user_sessions
        ],
        total_count=len(user_sessions)
    )


@router.delete("/sessions/{session_id}", response_model=schemas.SessionRevokeResponse)
async def revoke_specific_session(
    session_id: int,
    current_user = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(main.get_session_context)
):
    """
    Revoke a specific session by ID
    Allows users to logout from a specific device
    """
    # Get the session
    user_session = await session.get(services.models.Session, session_id)
    
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify the session belongs to the current user
    if str(user_session.user_uid) != str(current_user.uid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to revoke this session"
        )
    
    # Revoke the session
    user_session.is_active = False
    session.add(user_session)
    await session.commit()
    
    return schemas.SessionRevokeResponse(
        message="Session revoked successfully"
    )


# Admin-only endpoints

@router.get("/admin/sessions", response_model=schemas.SessionListResponse)
async def get_all_sessions(
    session: AsyncSession = Depends(main.get_session_context),
    _: bool = Depends(dependencies.RoleChecker(["admin"]))
):
    """
    Admin endpoint: Get all active sessions
    """
    from sqlmodel import select
    
    statement = select(services.models.Session).where(
        services.models.Session.is_active == True
    )
    result = await session.exec(statement)
    all_sessions = result.all()
    
    return schemas.SessionListResponse(
        sessions=[
            schemas.SessionResponse.model_validate(s)
            for s in all_sessions
        ],
        total_count=len(all_sessions)
    )


@router.post("/admin/revoke-user-sessions/{user_uid}", response_model=schemas.SessionRevokeResponse)
async def admin_revoke_user_sessions(
    user_uid: str,
    session: AsyncSession = Depends(main.get_session_context),
    _: bool = Depends(dependencies.RoleChecker(["admin"]))
):
    """
    Admin endpoint: Revoke all sessions for a specific user
    Useful for security incidents or user support
    """
    session_service = services.Session()
    revoked_count = await session_service.revoke_all_user_sessions(
        user_uid=user_uid,
        session=session
    )
    
    return schemas.SessionRevokeResponse(
        message=f"Revoked {revoked_count} session(s) for user {user_uid}"
    )