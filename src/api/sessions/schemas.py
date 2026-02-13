from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime
from typing import Optional


class SessionBase(BaseModel):
    """Base session fields"""
    user_uid: uuid.UUID
    expires_at: datetime
    is_active: bool = True


class SessionCreate(BaseModel):
    """Schema for creating a session (internal use)"""
    user_uid: uuid.UUID
    access_token: str
    refresh_token: str
    access_jti: str
    refresh_jti: str
    expires_at: datetime


class SessionResponse(BaseModel):
    """Schema for session responses to users"""
    id: int
    created_at: datetime
    expires_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class SessionDetailResponse(SessionResponse):
    """Detailed session info (admin only)"""
    user_uid: uuid.UUID
    access_jti: str
    refresh_jti: str
    
    model_config = ConfigDict(from_attributes=True)


class SessionListResponse(BaseModel):
    """Response for listing sessions"""
    sessions: list[SessionResponse]
    total_count: int


class SessionRevokeResponse(BaseModel):
    """Response when revoking sessions"""
    message: str