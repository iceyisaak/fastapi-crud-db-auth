"""
Additional endpoints for session management

Add these to your routes.py file to enable advanced session features
"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from . import services 
from ..auth import dependencies
from ...db import main
from sqlmodel.ext.asyncio.session import AsyncSession



router=APIRouter()




@router.get("/sessions")
async def get_active_sessions(
    current_user = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(main.get_session)
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
    return {
        "sessions": [
            {
                "id": s.id,
                "created_at": s.created_at.isoformat(),
                "expires_at": s.expires_at.isoformat(),
                "is_active": s.is_active
            }
            for s in user_sessions
        ],
        "total_count": len(user_sessions)
    }


@router.delete("/sessions/{session_id}")
async def revoke_specific_session(
    session_id: int,
    current_user = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(main.get_session)
):
    """
    Revoke a specific session by ID
    Allows users to logout from a specific device
    """
    session_service = services.Session()
    
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
    
    return JSONResponse(
        content={"message": "Session revoked successfully"},
        status_code=status.HTTP_200_OK
    )


# Admin-only endpoints (add role_checker for admin role)

@router.get("/admin/sessions")
async def get_all_sessions(
    session: AsyncSession = Depends(main.get_session),
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
    
    return {
        "sessions": [
            {
                "id": s.id,
                "user_uid": str(s.user_uid),
                "created_at": s.created_at.isoformat(),
                "expires_at": s.expires_at.isoformat()
            }
            for s in all_sessions
        ],
        "total_count": len(all_sessions)
    }


@router.post("/admin/revoke-user-sessions/{user_uid}")
async def admin_revoke_user_sessions(
    user_uid: str,
    session: AsyncSession = Depends(main.get_session),
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
    
    return JSONResponse(
        content={
            "message": f"Revoked {revoked_count} session(s) for user {user_uid}"
        },
        status_code=status.HTTP_200_OK
    )